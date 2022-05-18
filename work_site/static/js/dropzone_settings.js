const dz = new Dropzone(".dropzone", {

  // The configuration we've talked about above
  uploadMultiple: true,
  autoProcessQueue: false,
  addRemoveLinks: true,
  maxFiles: 2,
  acceptedFiles: ('.xlsx'),
  dictDefaultMessage: 'Umieść pliki SAP,INW tutaj',

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
        }
      });

