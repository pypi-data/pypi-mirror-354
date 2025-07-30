use itertools::{Either, Itertools};
use tombi_ast::{algo::ancestors_at_position, AstNode};
use tombi_document_tree::{IntoDocumentTreeAndErrors, TryIntoDocumentTree};
use tombi_schema_store::{SchemaContext, SchemaUrl};
use tower_lsp::lsp_types::{HoverParams, TextDocumentPositionParams};

use crate::{
    backend,
    hover::{get_hover_content, HoverContent},
};

#[tracing::instrument(level = "debug", skip_all)]
pub async fn handle_hover(
    backend: &backend::Backend,
    params: HoverParams,
) -> Result<Option<HoverContent>, tower_lsp::jsonrpc::Error> {
    tracing::info!("handle_hover");
    tracing::trace!(?params);

    let HoverParams {
        text_document_position_params:
            TextDocumentPositionParams {
                text_document,
                position,
            },
        ..
    } = params;

    let config = backend.config().await;

    if !config
        .lsp()
        .and_then(|server| server.hover.as_ref())
        .and_then(|hover| hover.enabled)
        .unwrap_or_default()
        .value()
    {
        tracing::debug!("`server.hover.enabled` is false");
        return Ok(None);
    }

    let position = position.into();
    let Some(root) = backend.get_incomplete_ast(&text_document.uri).await else {
        return Ok(None);
    };

    let source_schema = backend
        .schema_store
        .resolve_source_schema_from_ast(&root, Some(Either::Left(&text_document.uri)))
        .await
        .ok()
        .flatten();

    let (toml_version, _) = backend.source_toml_version(source_schema.as_ref()).await;

    let Some((keys, range)) = get_hover_keys_and_range(&root, position, toml_version).await else {
        return Ok(None);
    };

    if keys.is_empty() && range.is_none() {
        return Ok(None);
    }

    let document_tree = root.into_document_tree_and_errors(toml_version).tree;

    return Ok(get_hover_content(
        &document_tree,
        position,
        &keys,
        &SchemaContext {
            toml_version,
            root_schema: source_schema.as_ref().and_then(|s| s.root_schema.as_ref()),
            sub_schema_url_map: source_schema.as_ref().map(|s| &s.sub_schema_url_map),
            store: &backend.schema_store,
        },
    )
    .await
    .map(|mut content| {
        content.range = range;
        if let Some(schema_url) = content
            .schema_url
            .as_ref()
            .and_then(|url| get_tombi_github_schema_url(url))
        {
            content.schema_url = Some(schema_url);
        }
        content
    }));
}

pub(crate) async fn get_hover_keys_and_range(
    root: &tombi_ast::Root,
    position: tombi_text::Position,
    toml_version: tombi_config::TomlVersion,
) -> Option<(Vec<tombi_document_tree::Key>, Option<tombi_text::Range>)> {
    let mut keys_vec = vec![];
    let mut hover_range = None;

    for node in ancestors_at_position(root.syntax(), position) {
        if let Some(array) = tombi_ast::Array::cast(node.to_owned()) {
            for (value, comma) in array.values_with_comma() {
                if hover_range.is_none() {
                    let mut range = value.range();
                    if let Some(comma) = comma {
                        range += comma.range()
                    };
                    if range.contains(position) {
                        hover_range = Some(range);
                    }
                }
            }
        } else if let Some(inline_table) = tombi_ast::InlineTable::cast(node.to_owned()) {
            for (key_value, comma) in inline_table.key_values_with_comma() {
                if hover_range.is_none() {
                    let mut range = key_value.range();
                    if let Some(comma) = comma {
                        range += comma.range()
                    };
                    if range.contains(position) {
                        hover_range = Some(range);
                    }
                }
            }
        };

        let keys = if let Some(kv) = tombi_ast::KeyValue::cast(node.to_owned()) {
            if hover_range.is_none() {
                if let Some(inline_table) = tombi_ast::InlineTable::cast(node.parent().unwrap()) {
                    for (key_value, comma) in inline_table.key_values_with_comma() {
                        if hover_range.is_none() {
                            let mut range = key_value.range();
                            if let Some(comma) = comma {
                                range += comma.range()
                            };
                            if range.contains(position) {
                                hover_range = Some(range);
                                break;
                            }
                        }
                    }
                } else {
                    hover_range = Some(kv.range());
                }
            }
            kv.keys()
        } else if let Some(table) = tombi_ast::Table::cast(node.to_owned()) {
            let header = table.header();
            if let Some(header) = &header {
                if hover_range.is_none()
                    && (header
                        .keys()
                        .last()
                        .map_or(true, |key| key.syntax().range().contains(position))
                        || table
                            .leading_comments()
                            .any(|comment| comment.syntax().range().contains(position))
                        || table
                            .tailing_comment()
                            .is_some_and(|comment| comment.syntax().range().contains(position))
                        || table
                            .key_values_begin_dangling_comments()
                            .into_iter()
                            .any(|comments| {
                                comments
                                    .into_iter()
                                    .any(|comment| comment.syntax().range().contains(position))
                            })
                        || table
                            .key_values_end_dangling_comments()
                            .into_iter()
                            .any(|comments| {
                                comments
                                    .into_iter()
                                    .any(|comment| comment.syntax().range().contains(position))
                            }))
                {
                    hover_range = Some(table.syntax().range());
                }
            }

            header
        } else if let Some(array_of_table) = tombi_ast::ArrayOfTable::cast(node.to_owned()) {
            let header = array_of_table.header();
            if let Some(header) = &header {
                if hover_range.is_none()
                    && (header
                        .keys()
                        .last()
                        .map_or(true, |key| key.syntax().range().contains(position))
                        || array_of_table
                            .leading_comments()
                            .any(|comment| comment.syntax().range().contains(position))
                        || array_of_table
                            .tailing_comment()
                            .is_some_and(|comment| comment.syntax().range().contains(position))
                        || array_of_table
                            .key_values_begin_dangling_comments()
                            .into_iter()
                            .any(|comments| {
                                comments
                                    .into_iter()
                                    .any(|comment| comment.syntax().range().contains(position))
                            })
                        || array_of_table
                            .key_values_end_dangling_comments()
                            .into_iter()
                            .any(|comments| {
                                comments
                                    .into_iter()
                                    .any(|comment| comment.syntax().range().contains(position))
                            }))
                {
                    hover_range = Some(array_of_table.syntax().range());
                }
            }
            header
        } else if let Some(root) = tombi_ast::Root::cast(node.to_owned()) {
            if hover_range.is_none()
                && (root
                    .key_values_begin_dangling_comments()
                    .into_iter()
                    .any(|comments| {
                        comments
                            .into_iter()
                            .any(|comment| comment.syntax().range().contains(position))
                    })
                    || root
                        .key_values_end_dangling_comments()
                        .into_iter()
                        .any(|comments| {
                            comments
                                .into_iter()
                                .any(|comment| comment.syntax().range().contains(position))
                        }))
            {
                hover_range = Some(root.syntax().range());
            }
            continue;
        } else {
            continue;
        };

        let Some(keys) = keys else { continue };

        let keys = if keys.range().contains(position) {
            let mut new_keys = Vec::with_capacity(keys.keys().count());
            for key in keys
                .keys()
                .take_while(|key| key.token().unwrap().range().start <= position)
            {
                match key.try_into_document_tree(toml_version) {
                    Ok(Some(key)) => new_keys.push(key),
                    _ => return None,
                }
            }
            new_keys
        } else {
            let mut new_keys = Vec::with_capacity(keys.keys().count());
            for key in keys.keys() {
                match key.try_into_document_tree(toml_version) {
                    Ok(Some(key)) => new_keys.push(key),
                    _ => return None,
                }
            }
            new_keys
        };

        if hover_range.is_none() {
            hover_range = keys.iter().map(|key| key.range()).reduce(|k1, k2| k1 + k2);
        }

        keys_vec.push(keys);
    }

    Some((
        keys_vec.into_iter().rev().flatten().collect_vec(),
        hover_range,
    ))
}

pub(crate) fn get_hover_accessors(
    document_tree: &tombi_document_tree::DocumentTree,
    keys: &[tombi_document_tree::Key],
    position: tombi_text::Position,
) -> Vec<tombi_schema_store::Accessor> {
    let mut accessors: Vec<tombi_schema_store::Accessor> = Vec::new();
    let mut current_value: &tombi_document_tree::Value = document_tree.into();

    for key in keys {
        fn find_value_in_current<'a>(
            current_value: &'a tombi_document_tree::Value,
            key: &tombi_document_tree::Key,
            accessors: &mut Vec<tombi_schema_store::Accessor>,
            position: tombi_text::Position,
        ) -> &'a tombi_document_tree::Value {
            match current_value {
                tombi_document_tree::Value::Array(array) => {
                    for (index, value) in array.values().iter().enumerate() {
                        if value.range().contains(position) {
                            accessors.push(tombi_schema_store::Accessor::Index(index));
                            return find_value_in_current(value, key, accessors, position);
                        }
                    }
                }
                tombi_document_tree::Value::Table(table) => {
                    if let Some(value) = table.get(key) {
                        return value;
                    }
                }
                _ => {}
            }

            current_value
        }

        current_value = find_value_in_current(current_value, key, &mut accessors, position);
        accessors.push(tombi_schema_store::Accessor::Key(key.value().to_string()));
    }

    if let tombi_document_tree::Value::Array(array) = current_value {
        for (index, value) in array.values().iter().enumerate() {
            if value.range().contains(position) {
                accessors.push(tombi_schema_store::Accessor::Index(index));
                break;
            }
        }
    }

    accessors
}

pub fn get_tombi_github_schema_url(schema_url: &tower_lsp::lsp_types::Url) -> Option<SchemaUrl> {
    if schema_url.scheme() == "tombi" {
        let Some(schema_filename) = schema_url.path().strip_prefix("/json/schemas/") else {
            return None;
        };
        let version = env!("CARGO_PKG_VERSION");
        let branch = if version == "0.0.0-dev" {
            "main".to_string()
        } else {
            format!("refs/tags/v{version}")
        };
        let Ok(schema_url) = SchemaUrl::parse(&format!(
            "https://raw.githubusercontent.com/tombi-toml/tombi/{branch}/schemas/{schema_filename}"
        )) else {
            return None;
        };
        Some(schema_url)
    } else {
        None
    }
}
