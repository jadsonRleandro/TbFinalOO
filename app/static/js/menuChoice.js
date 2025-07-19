function verifythisform(img) {
    const form = img.closest('form');
    if (!form) return alert('Formulário não encontrado.');

    // Pega o nome da música dentro da mesma div .musics
    const name = img.closest('.musics').querySelector('.musicName').textContent.trim();

    // Remove input antigo se existir
    const old = form.querySelector('input[name="music_name"]');
    if (old) old.remove();

    // Cria input hidden só com o nome da música
    const input = document.createElement('input');
    input.type = 'hidden';
    input.name = 'music_name';
    input.value = name;
    form.appendChild(input);

    form.submit();
}