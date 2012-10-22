<?php
/**
 * @file
 * Process a query create the context.
 */


/**
 * Argument plugin that invoke the needed context.
 */
$plugin = array(
  'title' => t("Solr search query"),
  'description' => t('Creates a "The context of solr search results" from the arg.'),
  'context' => 'ascs_panels_context',
);

/**
 * Argument pluging processor.
 */
function ascs_panels_arguments($arg = NULL, $conf = NULL, $empty = FALSE) {
  // Allowed types. The default option is all.
  //$obj = lv_search_obj();
  //$default_type = $obj->content_types[0];
  //$type = arg(1);
  //if (!in_array($type, $obj->content_types)) {
  //  $type = $default_type;
  //}
  //$keys = trim(urldecode(arg(2)));
  //$data = array(
  //'type' => $type,
  //  'keys' => $keys,
  //);


  // Get a query, put it into a context to get a common data.
  return ctools_context_create('ascs_panels_context', $data);
}
