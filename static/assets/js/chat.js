$(document).ready(function() {
  var lastSeenChatId = 0;

  var chatTable = $('#chatTable').DataTable({
    'processing': true,
    'oLanguage': {
      'sProcessing': '<div style="top: 0"><img src="static/assets/img/loading.svg"></div>',
    },
    'data': [],
    'order': [[2, "asc"]],
    'pageLength': 5,
    'lengthMenu': [[5, 10, 25, 100, -1], [5, 10, 25, 100, "All"]],
    'columns': [
      {
        'title': 'Message',
        'render': $.fn.dataTable.render.ellipsis(256)
      },
      {
        'title': 'Name',
        'render': $.fn.dataTable.render.ellipsis(64)
      },
      {
        'title': '#'
      }
    ]
  });

  function getChatMessages() {
    $.get("api/chat/?lastSeenId=" + lastSeenChatId)
    .done(function(data) {
      var pageInfo = chatTable.page.info();
      var onLastPage = (pageInfo.page == pageInfo.pages - 1 || pageInfo.pages == 0);
      data.messages.forEach(function(message) {
        lastSeenChatId = Math.max(lastSeenChatId, message.id);
        chatTable.row.add([
          message.body,
          message.sender,
          message.id
        ]);
      });
      if (data.messages.length > 0) {
        chatTable.draw('full-hold'); // Research and order, but keep page
        if (onLastPage) {
          chatTable.page('last').draw('page');
        }
      }
      $(".hide-when-offline").show();
      setTimeout(getChatMessages, 0);
    })
    .fail(function(jqxhr, statusText, errorThrown) {
      console.log("Getting chat failed:", statusText, errorThrown);
      lastSeenChatId = 0;
      $(".hide-when-offline").hide();
      setTimeout(getChatMessages, 2000);
    });
  }

  // Send Chat Message
  $(document).on('submit', '#chatForm', function(e) {
    e.preventDefault();
    var $form = $(this);
    keyval.set('chatSender', $('#sender').val());
    $.post("api/chat/", {
      'sender': $('#sender').val(),
      'body': $('#body').val()
    })
    .done(function(data) {
      $("#body").val("");
      $("#chatAlert").addClass('d-none');
    })
    .fail(function(jqxhr, statusText, errorThrown) {
      $("#chatAlert").text("Failed to send").removeClass('d-none');
      console.log("Failed to send message", statusText, errorThrown);
    });
  });

  keyval = {
    'get': function(key, defaultValue) {
      if (window.localStorage) {
        var ret = window.localStorage.getItem(key);
        if (ret === null) return defaultValue;
        return ret;
      }
      return defaultValue;
    },
    'set': function(key, val) {
      if (window.localStorage) {
        localStorage.setItem(key, val);
      }
    }
  };

  setTimeout(getChatMessages, 0);
  $('#sender').val(keyval.get('chatSender', 'Anon'));

});
