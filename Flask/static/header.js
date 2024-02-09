 function showConfirmation() {
    var isLogout = window.confirm("ログアウトしますか？");
        
    // キャンセルした場合の処理
    if (!isLogout) {
        alert("キャンセルしました。");
        return;
    }

    confirmLogout(isLogout);
}

function cancelLogout() {
    alert("ログアウトしませんでした。");
    window.location.href = "/index";
}

function confirmLogout(isLogout) {
    if (isLogout) {
        fetch("/logout", { method: "POST" })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert("ログアウトしました。");
                    window.location.href = "/index";
                } else {
                    alert("ログアウトに失敗しました。");
                }
            });
    } else {
        cancelLogout();
    }
}

function logoutUser() {
    fetch("/logout", { method: "POST" })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("ログアウトしました。");
                window.location.href = "/index";
            } else {
                alert("ログアウトしていません。");
            }
        });
}

document.querySelector('.hamburger-menu').addEventListener('click', function () {
    document.querySelector('.menu').classList.toggle('active');
});
