<?php
/**
 * @file
 * Search results achieved from the Apache Solr service. Context plugin.
 */


/**
 * Describe a plugin.
 */
$plugin = array(
  'title' => t("Solr search results (ASCS)"),
  'description' => t('Search results achieved from the Apache Solr service. Context plugin.'),
  'context' => 'ascs_panels_context_create',
  'context name' => 'ascs_panels_context',
);


/**
 * Return empty context data.
 */
function _lv_search_empty_data() {
  return array(
    'keys' => "",
    'total_found' => 0,
    'data' => array(
      'article' => array(
        'label' => t('Articles'),
        'data' => array(),
        'num_found' => 0,
      ),
      'news' => array(
        'label' => t('Actualités'),
        'data' => array(),
        'num_found' => 0,
      ),
      'product' => array(
        'label' => t('Produits'),
        'data' => array(),
        'num_found' => 0,
      ),
    ),
  );
}

/**
 * Plugin constructor.
 */
function lv_search_context_solr_create($empty, $data = NULL, $conf = FALSE) {

  // Check $context cache.
  static $context = NULL;
  if ($context != NULL) {
    return $context;
  }
  $keys = $data['keys'];

  // Fill context info.
  $context = new ctools_context('lv_search_context_solr');
  $context->title = t("Solr search results");
  $context->plugin = 'lv_search_context_solr';

  // If we have got an empty search request, we return the empty data.
  if (empty($keys)) {
    $context->data = _lv_search_empty_data();
    $context->data['type'] = $data['type'];
    return $context;
  }

  // Default number of results.
  $number_of_results = array(
    'article' => 2,
    'news' => 2,
    'product' => 4,
  );

  if (array_key_exists($data['type'], $number_of_results)) {
    foreach ($number_of_results as $key => &$value) {
      $value = 1;
      if ($key == $data['type']) {
        $value = 20;
      }
    }
  }

  // Search process.
  $found = array();
  try {
    $found['article'] = lv_search_execute(
    array(
      'keys' => $keys,
      'page' => 0,
    ),
    'article',
    $number_of_results['article']
    );
    $found['news'] = lv_search_execute(
    array(
      'keys' => $keys,
      'page' => 0,
    ),
    'news',
    $number_of_results['news']
    );
    $found['product'] = lv_search_execute(
    array(
      'keys' => $keys,
      'page' => 0,
    ),
    'product',
    $number_of_results['product']
    );
  }
  catch (Exception $e) {
    watchdog('Apache Solr search in LV module', nl2br(check_plain($e->getMessage())), NULL, WATCHDOG_ERROR);
    apachesolr_failure(t('Solr search in LV module'), $search['keys']);
  }

  // Prepare variables for a template.
  // Products.
  $products = array();
  foreach ($found['product']['result'] as $item) {
    $products[] = array(
      'title' => $item['title'],
      'nid' => $item['fields']['nid']['value'],
      'image' => theme('imagecache', 'lv_search_product_131_162', $item['fields']['sm_field_product_image']['value'][0]),
      'tag' => $item['fields']['ts_vid_1_names']['value'],
    );
  }

  // Wrap settings.
  $max_chars_in_the_line = 35;
  $number_of_lines = 5;
  $string_at_end = ' ...';

  // Articles.
  $articles = array();
  foreach ($found['article']['result'] as $item) {
    $teaser = wordwrap(strip_tags($item['fields']['teaser']['value']), $max_chars_in_the_line, '{split}');
    $teaser = split('{split}', $teaser);
    $teaser = array_slice($teaser, 0, $number_of_lines);
    $teaser = join(' ', $teaser) . $string_at_end;
    if (!empty($item['fields']['sm_field_article_image']['value'][0])) {
      $image = theme('imagecache', 'lv_search_article_75_93', $item['fields']['sm_field_article_image']['value'][0]);
    }
    else {
      $image = '';
    }
    $articles[] = array(
      'title' => $item['title'],
      'nid' => $item['fields']['nid']['value'],
      'image' => $image,
      'teaser' => $teaser,
    );
  }

  // News.
  $news = array();
  foreach ($found['news']['result'] as $item) {
    $teaser = wordwrap(strip_tags($item['fields']['teaser']['value']), $max_chars_in_the_line, '{split}');
    $teaser = split('{split}', $teaser);
    $teaser = array_slice($teaser, 0, $number_of_lines);
    $teaser = join(' ', $teaser) . $string_at_end;
    if (!empty($item['fields']['sm_field_news_image']['value'][0])) {
      $image = theme('imagecache', 'lv_search_article_75_93', $item['fields']['sm_field_news_image']['value'][0]);
    }
    else {
      $image = '';
    }
    $news[] = array(
      'title' => $item['title'],
      'nid' => $item['fields']['nid']['value'],
      'image' => $image,
      'teaser' => $teaser,
    );
  }

  // Fill data.
  $context->data = array(
    'type' => $data['type'],
    'keys' => $keys,
    'total_found' => $found['article']['num_found'] + $found['product']['num_found'] + $found['news']['num_found'],
    'data' => array(
      'article' => array(
        'label' => t('Articles'),
        'data' => $articles,
        'num_found' => $found['article']['num_found'],
      ),
      'news' => array(
        'label' => t('Actualités'),
        'data' => $news,
        'num_found' => $found['news']['num_found'],
      ),
      'product' => array(
        'label' => t('Produits'),
        'data' => $products,
        'num_found' => $found['product']['num_found'],
      ),
    ),
  );

  // Return result.
  return $context;
}
