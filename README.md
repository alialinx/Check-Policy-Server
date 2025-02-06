Bu betik, gelen e-postaları PostgreSQL veritabanında depolanan kara listelerle karşılaştıran bir Postfix politika hizmetidir . Mesajları reddetmek veya kabul etmek için HELO dizelerini, gönderen e-postalarını, etki alanlarını ve uzantıları doğrular .

Özellikler
Kara listeye alınan göndericilere, etki alanlarına ve uzantılara göre e-postaları engeller .
Kara liste verilerini depolamak ve almak için PostgreSQL kullanır .
Tornado TCP sunucusu olarak çalışır 127.0.0.1:35355.
Alıcıya özel engelleme kurallarını destekler .
