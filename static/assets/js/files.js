$(document).ready(function() {
  var localTable = $('#localTable').DataTable({
    'processing': true,
    'oLanguage': {
      'sProcessing': '<div style="top: 0"><img src="static/assets/img/loading.svg"></div>',
    },
    'data': [],
    'order': [[0, "desc"]],
    'pageLength': 5,
    'lengthMenu': [[5, 10, 25, 100, -1], [5, 10, 25, 100, "All"]],
    'columns': [
      {
        'title': 'Name',
        'render': $.fn.dataTable.render.ellipsis(256)
      },
      {
        'title': 'Size'
      },
      {
        'title': 'Actions',
        'render': function(hash){
          // TODO Create buttons for download, delete, push/isOnServer
          return hash;
        }
      }
    ]
  });

  function addInitialLocalFiles() {
    if (!window.indexedDB) {
      alert('IndexedDB is required, please contact the developers to add support for older browsers'); // TODO Compatibility: Hide local file tools, let you upload and download straight from server
      return;
    }
    var idbOpen = window.indexedDB.open(["files", "hashes"], 1);
    idbOpen.onupgradeneeded = function (event) {
      var db = event.target.result;
      var objStoreFiles = db.createObjectStore("files", { autoIncrement : true });
      objStoreFiles.createIndex("hash", "hash", {unique: false});
      var objStoreHashes = db.createObjectStore("hashes", { keyPath: "hash" });
    };
    idbOpen.onerror = function(event) {
      alert("Failed to open db");
    };
    idbOpen.onsuccess = function(event) {
      var db = event.target.result;
      db.onerror = function(event) {
        alert("Database error: " + event.target.errorCode);
      };
      db.transaction("files").objectStore("files").openCursor().onsuccess = function(event) {
        var cursor = event.target.result;
        if (cursor) {
          var file = cursor.value;
          localTable.row.add([
            file.name,
            file.size,
            file.hash
          ]).draw('full-hold');
          cursor.continue();
        }
      };
    };
  }

  // Add files to local storage
  $(document).on('click', '#uploadButton', function(e) {
    $("#uploadInput").click();
  });

  $(document).on('change', '#uploadInput', function(e) {
    if (window.File && window.FileReader && window.FileList && window.Blob && window.indexedDB) {
      var files = e.target.files;
      var idbOpen = window.indexedDB.open(["files", "hashes"], 1);
      idbOpen.onerror = function(event) {
        alert("Failed to open db");
      };
      idbOpen.onsuccess = function(event) {
        var db = event.target.result;
        db.onerror = function(event) {
          alert("Database error: " + event.target.errorCode);
        };
        var filesList = [];
        for (var i = 0; i < files.length; i++) {
          filesList.push(files[i]);
        }
        filesList.forEach(function(file) {
          var fileReader = new FileReader();
          fileReader.readAsBinaryString(file);
          fileReader.onload = function(e) {
            var trans = db.transaction(['files', 'hashes'], 'readwrite');
            var hash = md5(e.target.result);
            var fileEntity = {
              'name': file.name,
              'size': file.size,
              'hash': hash
            };
            // TODO Check if hash is already in store, maybe index will catch it?
            // TODO Check if file name is already in use
            var hashEntity = {
              'hash': hash,
              'data': e.target.result
            };
            var addRequestFile = trans.objectStore('files').add(fileEntity);
            var addRequestHash = trans.objectStore('hashes').add(hashEntity);
            addRequestFile.onerror = function(eAddReq) {
              console.log("Failed to store file");
            };
            trans.oncomplete = function(eTrans) {
              localTable.row.add([
                fileEntity.name,
                fileEntity.size,
                hash
              ]).draw('full-hold');
            };

          };
        });
      }
    } else {
      alert('The File APIs are not fully supported in this browser.');
      // TODO Compatibility: Upload files directly to server
    }
  });

  setTimeout(addInitialLocalFiles, 0);

});
