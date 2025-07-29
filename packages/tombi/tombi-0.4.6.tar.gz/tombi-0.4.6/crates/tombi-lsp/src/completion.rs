mod comment;
mod completion_content;
mod completion_edit;
mod completion_kind;
mod hint;
mod schema_completion;
mod value;

use std::{borrow::Cow, ops::Deref};

use ahash::AHashMap;
use comment::get_comment_completion_contents;
pub use completion_content::CompletionContent;
pub use completion_edit::CompletionEdit;
use completion_kind::CompletionKind;
use futures::{future::BoxFuture, FutureExt};
pub use hint::CompletionHint;
use itertools::Itertools;
use tombi_ast::{algo::ancestors_at_position, AstNode};
use tombi_document_tree::{IntoDocumentTreeAndErrors, TryIntoDocumentTree};
use tombi_schema_store::{
    Accessor, CurrentSchema, ReferableValueSchemas, SchemaDefinitions, SchemaStore, SchemaUrl,
    ValueSchema,
};
use tombi_syntax::{SyntaxElement, SyntaxKind};
use tower_lsp::lsp_types::Url;

pub async fn get_completion_contents(
    root: tombi_ast::Root,
    position: tombi_text::Position,
    text_document_uri: &Url,
    schema_context: &tombi_schema_store::SchemaContext<'_>,
) -> Vec<CompletionContent> {
    let mut keys: Vec<tombi_document_tree::Key> = vec![];
    let mut completion_hint = None;

    for node in ancestors_at_position(root.syntax(), position) {
        tracing::trace!("node = {:?}", node);
        tracing::trace!(
            "prev_sibling_or_token() = {:?}",
            node.prev_sibling_or_token()
        );
        tracing::trace!(
            "next_sibling_or_token() = {:?}",
            node.next_sibling_or_token()
        );
        tracing::trace!("first_child_or_token() = {:?}", node.first_child_or_token());
        tracing::trace!("last_child_or_token() = {:?}", node.last_child_or_token());

        if let Some(SyntaxElement::Token(token)) = node.first_child_or_token() {
            if token.kind() == SyntaxKind::COMMENT && token.range().contains(position) {
                return get_comment_completion_contents(&root, position, text_document_uri);
            }
        }

        let ast_keys = if tombi_ast::Keys::cast(node.to_owned()).is_some() {
            if let Some(SyntaxElement::Token(last_token)) = node.last_child_or_token() {
                if last_token.kind() == SyntaxKind::DOT {
                    completion_hint = Some(CompletionHint::DotTrigger {
                        range: last_token.range(),
                    });
                }
            }
            continue;
        } else if let Some(kv) = tombi_ast::KeyValue::cast(node.to_owned()) {
            match (kv.keys(), kv.eq(), kv.value()) {
                (Some(_), Some(_), Some(_)) => {}
                (Some(_), Some(eq), None) => {
                    completion_hint = Some(CompletionHint::EqualTrigger { range: eq.range() });
                }
                (Some(keys), None, None) => {
                    if let Some(last_dot) = keys
                        .syntax()
                        .children_with_tokens()
                        .filter(|node_or_token| match node_or_token {
                            SyntaxElement::Token(token) => token.kind() == SyntaxKind::DOT,
                            _ => false,
                        })
                        .last()
                    {
                        completion_hint = Some(CompletionHint::DotTrigger {
                            range: last_dot.range(),
                        });
                    }
                }
                _ => {}
            }

            kv.keys()
        } else if let Some(table) = tombi_ast::Table::cast(node.to_owned()) {
            let (bracket_start_range, bracket_end_range) =
                match (table.bracket_start(), table.bracket_end()) {
                    (Some(bracket_start), Some(blacket_end)) => {
                        (bracket_start.range(), blacket_end.range())
                    }
                    _ => return Vec::with_capacity(0),
                };

            if position < bracket_start_range.start
                || (bracket_end_range.end <= position
                    && position.line == bracket_end_range.end.line)
            {
                return Vec::with_capacity(0);
            } else {
                if table.contains_header(position) {
                    completion_hint = Some(CompletionHint::InTableHeader);
                }
                table.header()
            }
        } else if let Some(array_of_table) = tombi_ast::ArrayOfTable::cast(node.to_owned()) {
            let (double_bracket_start_range, double_bracket_end_range) = {
                match (
                    array_of_table.double_bracket_start(),
                    array_of_table.double_bracket_end(),
                ) {
                    (Some(double_bracket_start), Some(double_bracket_end)) => {
                        (double_bracket_start.range(), double_bracket_end.range())
                    }
                    _ => return Vec::with_capacity(0),
                }
            };

            if position < double_bracket_start_range.start
                && (double_bracket_end_range.end <= position
                    && position.line == double_bracket_end_range.end.line)
            {
                return Vec::with_capacity(0);
            } else {
                if array_of_table.contains_header(position) {
                    completion_hint = Some(CompletionHint::InTableHeader);
                }
                array_of_table.header()
            }
        } else {
            continue;
        };

        let Some(ast_keys) = ast_keys else { continue };
        let mut new_keys = if ast_keys.range().contains(position) {
            let mut new_keys = Vec::with_capacity(ast_keys.keys().count());
            for key in ast_keys
                .keys()
                .take_while(|key| key.token().unwrap().range().start <= position)
            {
                match key.try_into_document_tree(schema_context.toml_version) {
                    Ok(Some(key)) => new_keys.push(key),
                    _ => return vec![],
                }
            }
            new_keys
        } else {
            let mut new_keys = Vec::with_capacity(ast_keys.keys().count());
            for key in ast_keys.keys() {
                match key.try_into_document_tree(schema_context.toml_version) {
                    Ok(Some(key)) => new_keys.push(key),
                    _ => return vec![],
                }
            }
            new_keys
        };

        new_keys.extend(keys);
        keys = new_keys;
    }

    let document_tree = root
        .into_document_tree_and_errors(schema_context.toml_version)
        .tree;

    let current_schema = schema_context.root_schema.and_then(|document_schema| {
        document_schema
            .value_schema
            .as_ref()
            .map(|value_schema| CurrentSchema {
                value_schema: Cow::Borrowed(value_schema),
                schema_url: Cow::Borrowed(&document_schema.schema_url),
                definitions: Cow::Borrowed(&document_schema.definitions),
            })
    });

    let completion_contents = document_tree
        .deref()
        .find_completion_contents(
            position,
            &keys,
            &[],
            current_schema.as_ref(),
            schema_context,
            completion_hint,
        )
        .await;

    // NOTE: If there are completion contents with the same priority,
    //       remove the completion contents with lower priority.
    completion_contents
        .into_iter()
        .fold(AHashMap::new(), |mut acc: AHashMap<_, Vec<_>>, content| {
            acc.entry(content.label.clone()).or_default().push(content);
            acc
        })
        .into_iter()
        .filter_map(|(_, contents)| {
            contents
                .into_iter()
                .sorted_by(|a, b| a.priority.cmp(&b.priority))
                .next()
        })
        .collect()
}

pub trait FindCompletionContents {
    fn find_completion_contents<'a: 'b, 'b>(
        &'a self,
        position: tombi_text::Position,
        keys: &'a [tombi_document_tree::Key],
        accessors: &'a [Accessor],
        current_schema: Option<&'a CurrentSchema<'a>>,
        schema_context: &'a tombi_schema_store::SchemaContext<'a>,
        completion_hint: Option<CompletionHint>,
    ) -> BoxFuture<'b, Vec<CompletionContent>>;
}

pub trait CompletionCandidate {
    fn title<'a: 'b, 'b>(
        &'a self,
        schema_url: &'a SchemaUrl,
        definitions: &'a SchemaDefinitions,
        schema_store: &'a SchemaStore,
        completion_hint: Option<CompletionHint>,
    ) -> BoxFuture<'b, Option<String>>;

    fn description<'a: 'b, 'b>(
        &'a self,
        schema_url: &'a SchemaUrl,
        definitions: &'a SchemaDefinitions,
        schema_store: &'a SchemaStore,
        completion_hint: Option<CompletionHint>,
    ) -> BoxFuture<'b, Option<String>>;

    async fn detail(
        &self,
        schema_url: &SchemaUrl,
        definitions: &SchemaDefinitions,
        schema_store: &SchemaStore,
        completion_hint: Option<CompletionHint>,
    ) -> Option<String> {
        self.title(schema_url, definitions, schema_store, completion_hint)
            .await
    }

    async fn documentation(
        &self,
        schema_url: &SchemaUrl,
        definitions: &SchemaDefinitions,
        schema_store: &SchemaStore,
        completion_hint: Option<CompletionHint>,
    ) -> Option<String> {
        self.description(schema_url, definitions, schema_store, completion_hint)
            .await
    }
}

trait CompositeSchemaImpl {
    fn title(&self) -> Option<String>;
    fn description(&self) -> Option<String>;
    fn schemas(&self) -> &ReferableValueSchemas;
}

impl<T: CompositeSchemaImpl + Sync + Send> CompletionCandidate for T {
    fn title<'a: 'b, 'b>(
        &'a self,
        schema_url: &'a SchemaUrl,
        definitions: &'a SchemaDefinitions,
        schema_store: &'a SchemaStore,
        completion_hint: Option<CompletionHint>,
    ) -> BoxFuture<'b, Option<String>> {
        async move {
            let mut candidates = ahash::AHashSet::new();
            {
                for referable_schema in self.schemas().write().await.iter_mut() {
                    if let Ok(Some(CurrentSchema {
                        value_schema,
                        schema_url,
                        definitions,
                    })) = referable_schema
                        .resolve(
                            Cow::Borrowed(schema_url),
                            Cow::Borrowed(definitions),
                            schema_store,
                        )
                        .await
                    {
                        if matches!(value_schema.as_ref(), ValueSchema::Null) {
                            continue;
                        }

                        if let Some(candidate) = CompletionCandidate::title(
                            value_schema.as_ref(),
                            &schema_url,
                            &definitions,
                            schema_store,
                            completion_hint,
                        )
                        .await
                        {
                            candidates.insert(candidate.to_string());
                        }
                    }
                }
            }
            if candidates.len() == 1 {
                return candidates.into_iter().next();
            }

            self.title().as_deref().map(|title| title.into())
        }
        .boxed()
    }

    fn description<'a: 'b, 'b>(
        &'a self,
        schema_url: &'a SchemaUrl,
        definitions: &'a SchemaDefinitions,
        schema_store: &'a SchemaStore,
        completion_hint: Option<CompletionHint>,
    ) -> BoxFuture<'b, Option<String>> {
        async move {
            let mut candidates = ahash::AHashSet::new();
            {
                for referable_schema in self.schemas().write().await.iter_mut() {
                    if let Ok(Some(CurrentSchema {
                        value_schema,
                        schema_url,
                        definitions,
                    })) = referable_schema
                        .resolve(
                            Cow::Borrowed(schema_url),
                            Cow::Borrowed(definitions),
                            schema_store,
                        )
                        .await
                    {
                        if matches!(value_schema.as_ref(), ValueSchema::Null) {
                            continue;
                        }

                        if let Some(candidate) = CompletionCandidate::description(
                            value_schema.as_ref(),
                            &schema_url,
                            &definitions,
                            schema_store,
                            completion_hint,
                        )
                        .await
                        {
                            candidates.insert(candidate.to_string());
                        }
                    }
                }
            }

            if candidates.len() == 1 {
                return candidates.into_iter().next();
            }

            self.description()
                .as_deref()
                .map(|description| description.into())
        }
        .boxed()
    }
}

fn tombi_json_value_to_completion_item(
    value: &tombi_json::Value,
    position: tombi_text::Position,
    detail: Option<String>,
    documentation: Option<String>,
    schema_url: Option<&SchemaUrl>,
    completion_hint: Option<CompletionHint>,
) -> Option<CompletionContent> {
    let (kind, value) = match value {
        tombi_json::Value::String(value) => (CompletionKind::String, format!("\"{value}\"")),
        tombi_json::Value::Number(value) => {
            if value.is_i64() {
                (CompletionKind::Integer, value.to_string())
            } else {
                (CompletionKind::Float, value.to_string())
            }
        }
        tombi_json::Value::Bool(value) => (CompletionKind::Boolean, value.to_string()),
        _ => return None,
    };

    Some(CompletionContent::new_default_value(
        kind,
        value.to_string(),
        detail,
        documentation,
        CompletionEdit::new_literal(&value, position, completion_hint),
        schema_url,
        None,
    ))
}
