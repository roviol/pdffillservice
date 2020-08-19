# pdffillservice
Flask Web Service for fill pdf form

## Ejecutar

```bash

docker-compose build
docker-compose up

```

## Uso
### php
```php
<?php
$postField = array();
$postFields['pdffile'] = curl_file_create(
    realpath('plantilla.pdf'), "mime", 'plantilla.pdf' );

$postFields['datafile'] = curl_file_create(
    realpath('data.json'), "mime", 'data.json' );

$headers = array("Content-Type" => "multipart/form-data");
$curl_handle = curl_init();
curl_setopt($curl_handle, CURLOPT_URL, "http://127.0.0.1:5000/pdf");
curl_setopt($curl_handle, CURLOPT_HTTPHEADER, $headers);
curl_setopt($curl_handle, CURLOPT_POST, TRUE);
curl_setopt($curl_handle, CURLOPT_POSTFIELDS, $postFields);
curl_setopt($curl_handle, CURLOPT_RETURNTRANSFER, TRUE);

$returned_data = curl_exec($curl_handle);
curl_close($curl_handle);
file_put_contents( "resultado.pdf", $returned_data) ;
?>
```

