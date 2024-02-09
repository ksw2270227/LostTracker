document.addEventListener('DOMContentLoaded', function() {
    var signupForm = document.getElementById('formid');

    // signupFormが存在するかどうかを確認
    if (signupForm) {
        signupForm.addEventListener('submit', function(e) {
            // デフォルトのフォーム送信を防止
            e.preventDefault();

            // ここにフォーム送信時のロジックを記述
            // 例: 入力値の検証、非同期リクエストの実行など

            // 例えば、入力された電話番号とメールアドレスを取得
            const phone = document.getElementById('phoneInput').value;
            const email = document.getElementById('emailInput').value;

            // サーバーに非同期リクエストを送信して、既存のユーザーかどうかをチェック
            fetch('/check_user', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ phone_number: phone, email_address: email })
            })
            .then(response => response.json())
            .then(data => {
                if (data.user_exists) {
                    // ユーザーが既に存在する場合は警告を表示
                    alert('同じ電話番号またはメールアドレスが既に登録されています。');
                } else {
                    // ユーザーが存在しない場合はフォームを送信
                    signupForm.submit();
                }
            })
            .catch((error) => {
                // エラー処理
                console.error('Error:', error);
            });

        });
    } else {
        // signupFormが存在しない場合はエラーメッセージを表示
        console.error('Signup form not found');
    }
});
