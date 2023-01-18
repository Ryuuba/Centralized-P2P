<?php
   if(isset($_POST['add'])) {
      $dbhost = 'localhost:3036';
      $dbuser = 'uriel';
      $dbpass = 'rootpassword';
      $conn = mysql_connect($dbhost, $dbuser, $dbpass);

      if(! $conn ) {
         die('Could not connect: ' . mysql_error());
      }

      if(! get_magic_quotes_gpc() ) {
         $product_name = addslashes ($_POST['product_name']);
         $product_manufacturer = addslashes ($_POST['product_name']);
      } else {
         $product_name = $_POST['product_name'];
         $product_manufacturer = $_POST['product_manufacturer'];
      }
      $ship_date = $_POST['ship_date'];
      $sql = "INSERT INTO products_tbl ".
         "(product_name,product_manufacturer, ship_date) ".
         "VALUES"."('$product_name','$product_manufacturer','$ship_date')";

      mysql_select_db('PRODUCTS');
      $retval = mysql_query( $sql, $conn );
      
      if(! $retval ) {
         die('Could not enter data: ' . mysql_error());
      }

      echo "Entered data successfully\n";
      mysql_close($conn);
   }
?>