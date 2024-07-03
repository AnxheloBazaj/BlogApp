
function showPhotoPreview(event) {
    var photoPreview = document.getElementById('photo-preview');
    var photoPreviewImg = document.getElementById('photo-preview-img');
    var reader = new FileReader();
    reader.onload = function () {
        if (reader.readyState == 2) {
            photoPreviewImg.src = reader.result;
            photoPreview.classList.remove('hidden');
        }
    }
    reader.readAsDataURL(event.target.files[0]);
}

function removePhoto() {
    var photoInput = document.getElementById('photo-input');
    var photoPreview = document.getElementById('photo-preview');
    var photoPreviewImg = document.getElementById('photo-preview-img');
    photoInput.value = '';
    photoPreviewImg.src = '';
    photoPreview.classList.add('hidden');
}

function toggleDropdown(event) {
    var dropdownMenu = event.target.nextElementSibling;
    dropdownMenu.classList.toggle('hidden');
}

document.addEventListener('DOMContentLoaded', (event) => {
    document.addEventListener('click', function (event) {
        var isClickInsideDropdown = event.target.closest('.dropdown-menu, .dropdown-toggle');
        var isClickInsideEditArea = event.target.closest('.edit-area, .dropdown-menu a');

        document.querySelectorAll('.dropdown-menu').forEach(function (menu) {
            if (!isClickInsideDropdown) {
                menu.classList.add('hidden');
            }
        });

        if (event.target.matches('.dropdown-toggle')) {
            var dropdownMenu = event.target.nextElementSibling;
            dropdownMenu.classList.toggle('hidden');
        }

        if (!isClickInsideEditArea) {
            document.querySelectorAll('.edit-area').forEach(function (editArea) {
                var postId = editArea.dataset.postId;
                document.getElementById('description-' + postId).classList.remove('hidden');
                document.getElementById('edit-form-' + postId).classList.add('hidden');
            });
        }
    });
});

function editPost(postId) {
    document.getElementById('description-' + postId).classList.add('hidden');
    document.getElementById('edit-form-' + postId).classList.remove('hidden');
}

function toggleUserDropdown() {
    document.getElementById('user-dropdown').classList.toggle('hidden');
}

document.addEventListener('click', function (event) {
    var isClickInsideDropdown = event.target.closest('#user-dropdown, .w-full.flex.items-center.justify-between');

    if (!isClickInsideDropdown) {
        document.getElementById('user-dropdown').classList.add('hidden');
    }
});
