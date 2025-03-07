const dz = new Dropzone(".dropzone", {

  // The configuration we've talked about above
  uploadMultiple: true,
  autoProcessQueue: false,
  addRemoveLinks: true,
  parallelUploads: 2,
  maxFiles: 2,
  acceptedFiles: ('.xlsx'),
  dictDefaultMessage: 'Umieść Tutaj!',

  init: function()
        {
          let myDropzone = this;
          /* 'submit-dropzone-btn' is the ID of the form submit button */
          document.getElementById('button').addEventListener("click", function (e) {
              e.preventDefault();
              myDropzone.processQueue();
          });

          this.on('sending', function(file, xhr, formData)
          {
             /* OPTION 2: Append inputs to FormData */
              formData.append("file", document.getElementById('button').value);
          });
          this.on('success', function(file, response) {
             window.location.href = JSON.parse(file.xhr.response).url
            });
          this.on('addedfile', function(file) {
            if (this.files.length > 2   ) {
            this.removeFile(this.files[0]);
            }
             });
        }
      });

