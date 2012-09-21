<?php

/**
 * Implementation of hook_node_info().
 */
function content_structure_node_info() {
  $items = array(
    'brand' => array(
      'name' => t('Brand'),
      'module' => 'features',
      'description' => t('A brand is a "Name, term, design, symbol, or any other feature that identifies one seller\'s good or service as distinct from those of other sellers."'),
      'has_title' => '1',
      'title_label' => t('Title'),
      'has_body' => '1',
      'body_label' => t('Body'),
      'min_word_count' => '0',
      'help' => '',
    ),
    'page' => array(
      'name' => t('Page'),
      'module' => 'features',
      'description' => t('A <em>page</em>, similar in form to a <em>story</em>, is a simple method for creating and displaying information that rarely changes, such as an "About us" section of a website. By default, a <em>page</em> entry does not allow visitor comments and is not featured on the site\'s initial home page.'),
      'has_title' => '1',
      'title_label' => t('Title'),
      'has_body' => '1',
      'body_label' => t('Body'),
      'min_word_count' => '0',
      'help' => '',
    ),
    'product' => array(
      'name' => t('Product'),
      'module' => 'features',
      'description' => t('In general, the product is defined as a "thing produced by labor or effort" or the "result of an act or a process", and stems from the verb produce, from the Latin prōdūce(re) \'(to) lead or bring forth\'. Since 1575, the word "product" has referred to anything produced. Since 1695, the word has referred to "thing or things produced.'),
      'has_title' => '1',
      'title_label' => t('Title'),
      'has_body' => '1',
      'body_label' => t('Body'),
      'min_word_count' => '0',
      'help' => '',
    ),
  );
  return $items;
}
