define([], function () {
    const FileManager = {
        triggerFileInput: function () {
            $('#fileInput').trigger('click');
        },

        submitFileUpload: function () {
            $('#fileUploadLocal').trigger('submit');
        },

        // New functions from main_new.js
        showPreviewOfAvatar: function () {
            const uploadFile = $(this);
            const files = this.files;

            if (files && files.length && window.FileReader) {
                const reader = new FileReader();
                reader.readAsDataURL(files[0]);

                reader.onloadend = function () {
                    uploadFile.closest("div").find('.ratio').html(`
                        <div class="w-100 h-100"
                             style="background-image: url(${this.result});
                                    background-size: cover;
                                    background-position: center;">
                        </div>
                    `);
                };
            }
        },

        cloneFromGit: function (e) {
            e.preventDefault();
            const form = $(e.target);
            const button = form.find('button[type="submit"]');
            const spinner = button.find('.spinner-border');
            const buttonText = button.find('span:not(.spinner-border)');
            const modal = form.closest('.modal');

            button.prop('disabled', true);
            spinner.removeClass('d-none');
            buttonText.text('Cloning...');

            $.ajax({
                url: form.attr('action'),
                method: 'POST',
                data: form.serialize(),
                success: function (response) {
                    $(modal).modal('hide');
                    $(form.closest('.tab-pane')).html(response);
                },
                error: function () {
                    button.removeClass('btn-primary').addClass('btn-danger');
                    buttonText.text('Clone Repository');
                },
                complete: function () {
                    spinner.addClass('d-none');
                    button.prop('disabled', false);
                }
            });
        },

        deleteFolder: function (e) {
            e.preventDefault();
            const button = $(this);
            const itemName = button.data('item-name');
            const itemType = button.data('item-type');

            if (confirm(`Do you want to delete ${itemType === 'folder' ? 'the folder' : 'the file'} "${itemName}"?`)) {
                $.ajax({
                    url: '/api/delete-folder',
                    method: 'DELETE',
                    data: {
                        path: button.data('item-path'),
                        projectname: button.data('projectname')
                    },
                    success: function (response) {
                        $(button.closest('.tab-pane')).html(response);
                    },
                    error: function () {
                        alert('Error deleting item.');
                    }
                });
            }
        },

        deleteXSLT: function (e) {
            e.preventDefault();
            const projectname = $(this).data('projectname');
            const self = this;
            $.ajax({
                url: `/delete-xslt/${projectname}`,
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                },
                success: function (response) {
                    FileManager.hideHint.call(self);
                },
                error: function () {
                    alert('Error deleting XSLT file.');
                }
            });
        },

        hideHint: function () {
            const hint = $('.xslt-upload');
            if (hint) {
                hint.addClass('d-none');
            }
        },

        selectNextcloudFolder: function () {
            const self = $(this);
            const new_state = self.is(':checked') ? 'checked' : '';
            const checkboxes = self.closest('.list-group-item').find('.nextcloud-folder');
            checkboxes
                .prop("checked", new_state)
                .not(':first')
                .prop("disabled", true);
        },

        dragDropHandler: function (event) {
            event.preventDefault();

            const dropZone = $(event.target).closest('.js-file-upload');
            const files = event.originalEvent.dataTransfer.files;
            const uploadUrl = dropZone.data('url');

            console.log(`Dropped ${files.length} files to upload`);

            if (files.length > 0) {
                // Create FormData with the dropped files
                const formData = new FormData();

                for (let i = 0; i < files.length; i++) {
                    formData.append('files', files[i]);
                    console.log(`File ${i + 1}: ${files[i].name}`);
                }

                // Upload files via AJAX
                $.ajax({
                    url: uploadUrl,
                    type: 'POST',
                    data: formData,
                    processData: false,
                    contentType: false,
                    success: function (response) {
                        dropZone.closest('.container, .tab-pane').html(response);
                    },
                    error: function (xhr, status, error) {
                        console.error('Upload error:', error);
                        dropZone.addClass('border-danger text-danger').removeClass('border-success');
                    }
                });
            }
        },

        preventDefaults: function (event) {
            event.preventDefault();
            event.stopPropagation();
        },

        // Update the init function to include drag & drop event listeners
        init: function () {
            $(document).on('change', 'input#fileInput', this.submitFileUpload);
            $(document).on('click', 'button#triggerFileInput', this.triggerFileInput);
            $(document).on('click', '.delete-folder', this.deleteFolder);
            $(document).on("change", ".showPreviewOfAvatar", this.showPreviewOfAvatar);
            $(document).on('click', '#deleteXsltButton', this.deleteXSLT);
            $(document).on('change', '.xslt-upload', this.hideHint);
            $(document).on('click', 'input.nextcloud-folder', this.selectNextcloudFolder);

            // Drag & Drop event listeners for elements with class 'js-file-upload'
            $(document).on('dragenter', '.js-file-upload', this.preventDefaults);
            $(document).on('dragover', '.js-file-upload', this.preventDefaults);
            $(document).on('dragleave', '.js-file-upload', this.preventDefaults);
            $(document).on('drop', '.js-file-upload', this.dragDropHandler);
            $(document).on('click', '.js-file-upload', function (event) {
                $('#triggerFileInput').click();
            })
        }
    };

    return FileManager;
});