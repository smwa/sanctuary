$(document).ready(function() {
  var lastSeenFileId = 0;

  var filesTable = $('#filesTable').DataTable({
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
        'render': $.fn.dataTable.render.ellipsis(40)
      },
      {
        'title': 'Size',
        'render': function (data, type) { if (type === 'display') return _formatBytes(data); return data; }
      },
      {
        'title': 'Download',
        'orderable': false,
        'render': function(id){
          var quotedUrl = '"api/files/' + id + '/"';
          return '<div class="btn-group">'
          + '<a target="_blank" class="btn btn-secondary" href=' + quotedUrl + '>Download</a>'
          + '</div>';
        }
      }
    ]
  });

  $('#fileInput').fileupload({
    url: 'api/files/',
    done: function (e, data) {
      $(".progressContainer").addClass('d-none');
    },
    progressall: function (e, data) {
      $(".progressContainer.d-none").removeClass('d-none');
      var progress = parseInt(data.loaded / data.total * 100, 10);
      $('#progress .progress-bar').css(
        'width',
         progress + '%'
      );
    }
  }).prop('disabled', !$.support.fileInput).parent().addClass($.support.fileInput ? undefined : 'disabled');

  function getNewFiles() {
    $.get("api/files/?lastSeenId=" + lastSeenFileId)
    .done(function(data) {
      data.files.forEach(function(file) {
        lastSeenFileId = file.id;
        filesTable.row.add([
          file.name,
          file.size,
          file.id
        ]);
      });
      if (data.files.length > 0) {
        filesTable.draw('full-hold'); // Research and order, but keep page
      }
      setTimeout(getNewFiles, 2000);
    })
    .fail(function(jqxhr, statusText, errorThrown) {
      lastSeenFileId = 0;
      filesTable.clear().draw();
      console.log("Getting files failed:", statusText, errorThrown);
      setTimeout(getNewFiles, 2000);
    });    
  }

  function _formatBytes(bytes) {
    var modifiableBytes = bytes;
    var sizes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB'];
    for (size in sizes) {
      if (bytes < 1024) {
        return Math.round(bytes) + " " + sizes[size];
      }
      bytes /= 1024;
    }
    return bytes + " " + sizes[0];
  }

  setTimeout(getNewFiles, 0);

});
