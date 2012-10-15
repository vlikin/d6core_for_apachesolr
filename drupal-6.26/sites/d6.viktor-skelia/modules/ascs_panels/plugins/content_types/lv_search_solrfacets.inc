<?php
/**
 * @file
 * CCT block - Apache Solr a short search result information.
 */

$plugin = array(
  'title' => t('LV Solr facets.'),
  'description' => t('Search results achieved from Apache Solr service. Left side block with facets.'),
  'content_types' => 'lv_search_lv_search_cct_solrfacets',
  'single' => TRUE,
  'render callback' => 'lv_search_lv_search_cct_solrfacets_render',
  'edit form' => 'lv_search_lv_search_cct_solrfacets_edit_form',
  'admin title' => 'lv_search_lv_search_cct_solrfacets_admin_title',
  'required context' => new ctools_context_required(t('Apache Solr data'), 'lv_search_context_solr'),
  'category' => t('LV'),
);

/**
 * Returns an edit form for the custom type.
 *
 * This is required to get access to the context.
 */
function lv_search_lv_search_cct_solrfacets_edit_form(&$form, &$form_state) {
  $conf = $form_state['conf'];
  $form['conf'] = array(
    '#tree' => TRUE,
  );
}

/**
 * Presubmit handler.
 *
 * This is required to get access to the context.
 */
function lv_search_lv_search_cct_solrfacets_edit_form_submit(&$form, &$form_state) {
  $form_state['conf'] = $form_state['values']['conf'];
}

/**
 * Admin title callback.
 */
function lv_search_lv_search_cct_solrfacets_admin_title($subtype, $conf, $context) {
  return t('Solr search results with facets.');
}

/**
 * Render callback.
 */
function lv_search_lv_search_cct_solrfacets_render($subtype, $conf, $panel_args, $context) {
  $block = new stdClass();
  $block->content = theme('lv_search_result_left', $context->data);
  return $block;
}
