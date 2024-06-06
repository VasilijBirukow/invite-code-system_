document.addEventListener('DOMContentLoaded', async (event) => {
    await fillUserData(userPhone);
});

async function fillUserData(phone) {
    let response = await fetch('/user-data?phone=' + phone);
    if (response.ok) {
        let json = await response.json();
        document.getElementById('user_phone_container').textContent = 'Номер телефона: ' + json.user.number;
        document.getElementById('generated_invite_code_container').textContent = 'Сгенерированный код: ' + (json.user.generated_code);
        updateAppliedCodeContainer(json.user.applied_code);

        let listHtml = json.users_login_list.map(login => `<li>${login}</li>`).join('');
        document.getElementById('code_users_container').innerHTML = `<ul>${listHtml}</ul>`;
    } else {
        alert("Ошибка HTTP: " + response.status);
    }
}

function updateAppliedCodeContainer(appliedCode) {
    const container = document.getElementById('applied_invite_code_container');
    if (appliedCode) {
        container.textContent = 'Применённый код: ' + appliedCode;
    } else {
        container.innerHTML = `
            <div class="user-input">
                <input type="text" id="apply_code_input" placeholder="Введите код">
                <button onclick="applyCode()">Применить</button>
            </div>
        `;
    }
}


async function applyCode() {
    const applyButton = document.querySelector('#applied_invite_code_container button')
    const input = document.getElementById('apply_code_input');
    const code = input.value;
    applyButton.disabled = true;

    let response = await fetch('/check-applied-code?code=' + code + '&phone=' + userPhone);

    if (response.ok) {
        updateAppliedCodeContainer(code);
    } else if (response.status === 400) {
        alert('Неверный код.');
        input.value = '';
    } else {
        alert('Ошибка сервера. Попробуйте позже.');
    }

    applyButton.disabled = false;
}
