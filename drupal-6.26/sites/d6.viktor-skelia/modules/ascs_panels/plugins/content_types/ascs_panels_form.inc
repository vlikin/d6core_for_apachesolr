<?php
/**
 * @file
 * CCT block - The search form.
 *
 * It contains a simple input with the submit button. The main idea is to get POST
 * data and redirect it to the search page with GET parameters..
 */

$plugin = array(
  'title' => t('ASCS search form.'),
  'description' => t('It contains a simple input with the submit button.
    The main idea is to get POST data and redirect it
    to the search page with GET parameters..
  '),
  'content_types' => 'ascs_panels_ascs_panels_form',
  'single' => TRUE,
  'render callback' => 'ascs_panels_ascs_panels_form_render',
  'edit form' => 'ascs_panels_ascs_panels_form_edit_form',
  'admin title' => 'ascs_panels_ascs_panels_form_admin_title',
  //'required context' => new ctools_context_required(t('Apache Solr data'), 'lv_search_context_solr'),
  'category' => t('ASCS'),
);

/**
 * Returns an edit form for the custom type.
 *
 * This is required to get access to the context.
 */
function ascs_panels_ascs_panels_form_edit_form(&$form, &$form_state) {
  $conf = $form_state['conf'];
  $form['conf'] = array(
    '#tree' => TRUE,
    'path_pattern' => array(
      '#type' => 'textfield',
      '#title' => t('Path pattern'),
      '#description' => t('
        Use :keywords placeholder defining the place of a search query location.
      '),
      '#default_value' => $conf['path_pattern'],
    ),
  );
}

/**
 * Presubmit handler.
 *
 * This is required to get access to the context.
 */
function ascs_panels_ascs_panels_form_edit_form_submit(&$form, &$form_state) {
  $form_state['conf'] = $form_state['values']['conf'];
}

/**
 * Admin title callback.
 */
function ascs_panels_ascs_panels_form_admin_title($subtype, $conf, $context) {
  return t('The search form.');
}

/**
 * Render callback.
 */
function ascs_panels_ascs_panels_form_render($subtype, $conf, $panel_args, $context) {
  $block = new stdClass();
  $block->content = drupal_get_form('ascs_panels_ascs_panels_form__form', $conf);
  return $block;
}

/**
 * It defines a search form.
 */
function ascs_panels_ascs_panels_form__form(&$form_state, $conf) {
  $form = array(
    '#attributes' => array(
      'class' => 'search',
    ),
    'keywords' => array(
      '#type' => 'textfield',
      '#size' => 30,
      '#attributes' => array(
        'class' => 'form-text field-search',
        'type' => 'text',
        'title' => t('Search form'),
        'placeholder' => t('Keywords, ...'),
      ),
      '#default_value' => $form_state['values']['keywords']
    ),
    'path_pattern' => array(
      '#type' => 'hidden',
      '#default_value' => $conf['path_pattern'],
    ),
    'submit' => array(
      '#type' => 'submit',
      '#value' => t('Search'),
    ),
  );
  return $form;
}


/**
 * It processes submit data of the search form.
 */
function ascs_panels_ascs_panels_form__form_submit($form, &$form_state) {
  // Redirect to the search results page.
  $redirect_to = str_replace(":keywords", urlencode($form_state['values']['keywords']), $form_state['values']['path_pattern']);
  drupal_goto($redirect_to);
}
