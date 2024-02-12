-- users テーブルの作成
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    user_name TEXT NOT NULL,
    full_name TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    email_address TEXT,
    password TEXT NOT NULL,
    age INTEGER,
    gender TEXT NOT NULL,
    current_event_id INTEGER,
    current_group_id INTEGER,
    user_status TEXT
);

-- admins テーブルの作成
CREATE TABLE admins (
    user_id INTEGER PRIMARY KEY,
    user_name TEXT NOT NULL,
    password TEXT NOT NULL,
    full_name TEXT NOT NULL,
    email_address TEXT NOT NULL
);

-- companies テーブルの作成
CREATE TABLE companies (
    company_id INTEGER PRIMARY KEY,
    company_name TEXT NOT NULL,
    company_password TEXT NOT NULL,
    address TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    email_address TEXT NOT NULL
);

-- companies_employee テーブルの作成
CREATE TABLE companies_employee (
    company_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    user_name TEXT NOT NULL,
    full_name TEXT NOT NULL,
    password TEXT NOT NULL,
    email_address TEXT NOT NULL,
    FOREIGN KEY (company_id) REFERENCES companies(company_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE groups (
    group_id INTEGER PRIMARY KEY,
    group_name TEXT NOT NULL,
    password TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    creation_date TEXT NOT NULL,
    max_members INTEGER NOT NULL,
    current_members INTEGER NOT NULL,
    event_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);


-- events テーブルの作成
CREATE TABLE events (
    company_id INTEGER NOT NULL,
    event_name TEXT NOT NULL,
    event_id INTEGER PRIMARY KEY,
    password TEXT NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    location TEXT NOT NULL,
    event_content TEXT NOT NULL,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

-- messages テーブルの作成
CREATE TABLE messages (
    message_id INTEGER PRIMARY KEY,
    sender_user_id INTEGER NOT NULL,
    sender_role TEXT NOT NULL,
    receiver_user_id INTEGER NOT NULL,
    receiver_role TEXT NOT NULL,
    message_content TEXT NOT NULL,
    sent_time TEXT NOT NULL,
    FOREIGN KEY (sender_user_id) REFERENCES users(user_id),
    FOREIGN KEY (receiver_user_id) REFERENCES users(user_id),
    FOREIGN KEY (sender_user_id) REFERENCES admins(admin_id),
    FOREIGN KEY (sender_user_id) REFERENCES admins(admin_id)
);

-- location_data テーブルの作成
CREATE TABLE location_data (
    user_id INTEGER NOT NULL,
    user_status TEXT NOT NULL,
    current_latitude REAL NOT NULL,
    current_longitude REAL NOT NULL,
    current_altitude REAL NOT NULL,
    acquisition_time TEXT NOT NULL,
    PRIMARY KEY (user_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- location_history テーブルの作成
CREATE TABLE location_history (
    user_id INTEGER NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    altitude REAL NOT NULL,
    acquisition_time TEXT NOT NULL,
    user_status TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);


-- `users` テーブルの初期値を設定
INSERT INTO users (user_id, user_name, full_name, phone_number, email_address, password, age, gender, current_event_id, current_group_id, user_status) VALUES
(1, 'hanako123', '花子 山田', '090-1234-5678', 'hanako@example.com', 'pass1234', 28, '女性', 3, 1, '通常'),
(2, 'taro2023', '太郎 佐藤', '080-9876-5432', 'taro@example.com', 'pass2023', 32, '男性', 1, 2, '待機'),
(3, 'sakura_flower', 'さくら 鈴木', '070-1111-2222', 'sakura@example.com', 'sakura123', 25, '女性', 2, 3, '迷子'),
(4, 'yamamoto_k', '健一 山本', '075-3333-4444', 'yamamoto@example.com', 'yama2024', 45, '男性', 4, 4, '緊急'),
(5, 'akira_tech', '明 秋田', '092-5555-6666', 'akira@example.com', 'akira5678', 30, '男性', 5, 5, '通常'),
(6, 'some123', '染 谷', '030-1334-3378', 'someya@example.com', 'pass12345', 111, '男性', 3, 1, '通常'),
(7, 'miyuki_star', '美幸 伊藤', '091-2345-6789', 'miyuki@example.com', 'miyu1234', 27, '女性', 2, 2, '待機'),
(8, 'hiroki_pro', '博樹 中村', '081-9876-5433', 'hiroki@example.com', 'hiro2023', 33, '男性', 1, 2, '迷子'),
(9, 'ayumi_sky', 'あゆみ 小林', '071-1111-2233', 'ayumi@example.com', 'ayu12345', 26, '女性', 3, 2, '通常');


INSERT INTO admins (user_id, user_name, password, full_name, email_address) VALUES
(1, 'admin_tanaka', 'admtanaka1', '田中 一郎', 'tanaka_admin@example.com'),
(2, 'admin_yamada', 'admyamada2', '山田 花子', 'yamada_admin@example.com'),
(3, 'admin_sato', 'admsato3', '佐藤 太郎', 'sato_admin@example.com'),
(4, 'admin_suzuki', 'admsuzuki4', '鈴木 さくら', 'suzuki_admin@example.com'),
(5, 'admin_nakamura', 'admnakam5', '中村 雄大', 'nakamura_admin@example.com');

INSERT INTO companies (company_id, company_name, company_password, address, phone_number, email_address) VALUES
(1, '株式会社山田', 'yamada123', '東京都渋谷区1-2-3', '03-1234-5678', 'contact@yamada.co.jp'),
(2, '鈴木工業株式会社', 'suzuki456', '大阪府大阪市北区4-5-6', '06-9876-5432', 'info@suzuki-ind.co.jp'),
(3, '佐藤電機株式会社', 'sato789', '愛知県名古屋市中区7-8-9', '052-1111-2222', 'support@sato-electric.co.jp'),
(4, '田中商事株式会社', 'tanaka000', '福岡県福岡市博多区10-11-12', '092-3333-4444', 'sales@tanaka-trading.co.jp'),
(5, '秋田システムズ株式会社', 'akita999', '北海道札幌市中央区13-14-15', '011-5555-6666', 'service@akita-systems.co.jp');

INSERT INTO companies_employee (company_id, user_id, user_name, full_name, password, email_address) VALUES
(1, 1, 'employee1', '山田 花子', 'emp1pass', 'hanako@yamada.co.jp'),
(2, 2, 'employee2', '佐藤 太郎', 'emp2pass', 'taro@suzuki-ind.co.jp'),
(3, 3, 'employee3', '鈴木 さくら', 'emp3pass', 'sakura@sato-electric.co.jp'),
(4, 4, 'employee4', '田中 健一', 'emp4pass', 'kenichi@tanaka-trading.co.jp'),
(5, 5, 'employee5', '秋田 明', 'emp5pass', 'akira@akita-systems.co.jp');

-- `groups` テーブルの初期値を設定
INSERT INTO groups (group_id, group_name, password, user_id, creation_date, max_members, current_members, event_id) VALUES
(1, 'Group Alpha', 'grouppass1', 1, '2023-11-17 10:00:00', 10, 2, 1),
(2, 'Group Beta', 'grouppass2', 2, '2023-11-18 11:00:00', 15, 4, 2),
(3, 'Group Gamma', 'grouppass3', 3, '2023-11-19 12:00:00', 20, 1, 3),
(4, 'Group Delta', 'grouppass4', 4, '2023-11-20 13:00:00', 12, 1, 4),
(5, 'Group Epsilon', 'grouppass5', 5, '2023-11-21 14:00:00', 8, 1, 5);

INSERT INTO events (company_id, event_name, event_id, password, start_time, end_time, location, event_content) VALUES
(1, '新製品発表会', 1, 'eventpass1', '2023-12-01 09:00:00', '2023-12-01 18:00:00', '東京国際フォーラム', '最新技術の展示とデモンストレーション'),
(2, '技術交流会', 2, 'eventpass2', '2023-12-05 10:00:00', '2023-12-05 17:00:00', '大阪サイエンスミュージアム', '業界リーダーとのネットワーキングイベント'),
(3, 'エコロジーイノベーションサミット', 3, 'eventpass3', '2023-12-10 08:30:00', '2023-12-10 19:00:00', '名古屋国際会議場', '持続可能な技術の開発と応用'),
(4, 'エンジニアリングフェア', 4, 'eventpass4', '2023-12-15 09:00:00', '2023-12-15 20:00:00', '福岡サンパレス', 'エンジニアリングの最新トレンドと展望'),
(5, 'ITセキュリティカンファレンス', 5, 'eventpass5', '2023-12-20 10:00:00', '2023-12-20 18:00:00', '札幌コンベンションセンター', 'サイバーセキュリティの最新動向と対策'),
(6,'国際スイカ大食い大会',6,'SUIKA2024','2023-12-05 10:00:00','2023-12-05 10:00:00','熊本県熊本市中央区本丸１−１','世界が熱狂したこの大会が３年ぶりに復活');

INSERT INTO messages (message_id, sender_user_id, sender_role, receiver_user_id, receiver_role, message_content, sent_time) 
VALUES
(1, 1, 'User', 2, 'Admin', 'こんにちは、問題が発生しています。', '2024-01-19 10:00:00'),
(2, 2, 'Admin', 1, 'User', 'こんにちは、どのような問題でしょうか？', '2024-01-19 10:02:00'),
(3, 1, 'User', 2, 'Admin', 'アカウントにログインできません。', '2024-01-19 10:05:00'),
(4, 2, 'Admin', 1, 'User', 'ユーザー名とパスワードを再確認してください。', '2024-01-19 10:07:00'),
(5, 1, 'User', 2, 'Admin', 'ありがとうございます、解決しました！', '2024-01-19 10:10:00');


INSERT INTO location_data (user_id, user_status, current_latitude, current_longitude, current_altitude, acquisition_time) VALUES
(1, '通常', 35.6895, 139.6917, 40.0, '2023-11-17 09:00:00'),  -- 東京
(2, '待機', 34.6937, 135.5022, 30.0, '2023-11-17 09:15:00'),  -- 大阪
(3, '迷子', 35.6895, 139.6917, 45.0, '2023-11-17 09:30:00'),  -- 東京
(4, '緊急', 43.0618, 141.3545, 20.0, '2023-11-17 09:45:00'),  -- 札幌
(5, '通常', 26.2124, 127.6809, 15.0, '2023-11-17 10:00:00'),  -- 沖
(6, '通常', 35.6897, 139.6921, 50.0, '2023-11-17 09:05:00'),  -- 東京
(7, '待機', 35.4148, 139.4501, 25.0, '2023-11-17 09:20:00'),  -- 神奈川県
(8, '迷子', 35.6896, 139.7004, 35.0, '2023-11-17 09:35:00'),  -- 東京
(9, '緊急', 35.8579, 139.6489, 45.0, '2023-11-17 09:50:00');  -- 埼玉県

INSERT INTO location_history (user_id, latitude, longitude, altitude, acquisition_time, user_status) VALUES
(1, 35.6895, 139.6917, 40.0, '2023-11-17 08:00:00', '通常'),  -- 東京の位置情報
(2, 34.6937, 135.5022, 30.0, '2023-11-17 08:15:00', '待機'),  -- 大阪の位置情報
(3, 35.6895, 139.6917, 45.0, '2023-11-17 08:30:00', '迷子'),  -- 東京の位置情報
(4, 43.0618, 141.3545, 20.0, '2023-11-17 08:45:00', '緊急'),  -- 札幌の位置情報
(5, 26.2124, 127.6809, 15.0, '2023-11-17 09:00:00', '通常');  -- 沖縄の位置情報

