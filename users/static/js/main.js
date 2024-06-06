function extractNumbers(str) {
    return str.replace(/\D/g, '');
}

async function sendVerificationCode() {
    const phoneInput = document.getElementById('phone');
    const phone = extractNumbers(phoneInput.value);
    const response = await fetch('/auth/?phone=' + phone);
    if (response.status === 200) {
        let code = Math.floor(1000 + Math.random() * 9000);
        // code = code.toString().substring(0, 4);
        alert(`Вводим код подтверждения: ${code}`);
        const currentUrl = window.location.href
        const newUrl = currentUrl.replace('/auth-page/', '/profile/');
        await new Promise(resolve => setTimeout(resolve, 3000));
        window.location.href = newUrl + '?phone=' + phone;
    } else {
        alert(`Номер не корректен`);
    }
}
