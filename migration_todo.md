- мигрировать старые favicons в новый сайт: там были сделаны favicons под разные устройства и в странице они включались блоком:
```
<link rel="apple-touch-icon" sizes="57x57" href="/old/staticvicon/apple-touch-icon-57x57.png">
    <link rel="apple-touch-icon" sizes="60x60" href="/old/staticvicon/apple-touch-icon-60x60.png">
    <link rel="apple-touch-icon" sizes="72x72" href="/old/staticvicon/apple-touch-icon-72x72.png">
    <link rel="apple-touch-icon" sizes="76x76" href="/old/staticvicon/apple-touch-icon-76x76.png">
    <link rel="apple-touch-icon" sizes="114x114" href="/old/staticvicon/apple-touch-icon-114x114.png">
    <link rel="apple-touch-icon" sizes="120x120" href="/old/staticvicon/apple-touch-icon-120x120.png">
    <link rel="apple-touch-icon" sizes="144x144" href="/old/staticvicon/apple-touch-icon-144x144.png">
    <link rel="apple-touch-icon" sizes="152x152" href="/old/staticvicon/apple-touch-icon-152x152.png">
    <link rel="apple-touch-icon" sizes="180x180" href="/old/staticvicon/apple-touch-icon-180x180.png">
    <link rel="icon" type="image/png" href="/old/staticvicon/favicon-32x32.png" sizes="32x32">
    <link rel="icon" type="image/png" href="/old/staticvicon/android-chrome-192x192.png" sizes="192x192">
    <link rel="icon" type="image/png" href="/old/staticvicon/favicon-96x96.png" sizes="96x96">
    <link rel="icon" type="image/png" href="/old/staticvicon/favicon-16x16.png" sizes="16x16">
    <link rel="manifest" href="/old/staticvicon/manifest.json">
    <link rel="shortcut icon" href="/old/staticvicon/favicon.ico">
    <meta name="msapplication-TileColor" content="#da532c">
    <meta name="msapplication-TileImage" content="/static/img/favicon/mstile-144x144.png">
    <meta name="msapplication-config" content="/static/img/favicon/browserconfig.xml">
    <meta name="theme-color" content="#ffffff">
```


- мигрировать gtag

- проверить везде open graph на всех страницах: где надо запросить и вставить описнаия (все только по-английски)

- кнопки Share: - перести на более модерновую статическую js библиотеку, добавить актуальные в арт-кругах соцсети в эти кнопк 