divVacantRoom = document.getElementById('div_vacant_room')
if(divVacantRoom) {
    const value = divVacantRoom.vacantRoom;
    const div_a = document.getElementById('pointerEvent');
    const errorText = document.getElementById('errorVacantRoom')

    if (value == 0) {
        errorText.style.display = 'block';
        if(div_a) {
            div_a.style.pointerEvents = "none";
            div_a.querySelector('a').classList.remove('text-primary');
            div_a.querySelector('a').classList.remove('border-secondary');
            div_a.querySelector('a').classList.add('border-dark');
        }
    } else {
        errorText.style.display = 'none';
        if(div_a) {
            div_a.style.pointerEvents = 'auto';
            div_a.querySelector('a').classList.add('text-primary');
            div_a.querySelector('a').classList.remove('border-dark');
            div_a.querySelector('a').classList.add('border-secondary');
        }
    }
}
