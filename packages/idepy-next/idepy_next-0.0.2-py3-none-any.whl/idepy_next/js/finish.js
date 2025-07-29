window.idepy._createApi(JSON.parse('%(functions)s'));

if (window.idepy.platform == 'qtwebengine') {
  new QWebChannel(qt.webChannelTransport, function(channel) {
      window.idepy._QWebChannel = channel;
      window.dispatchEvent(new CustomEvent('idepyready'));
      window.dispatchEvent(new CustomEvent('pywebviewready'));
  });
} else {
  window.dispatchEvent(new CustomEvent('idepyready'));
  // 兼容原版
  window.pywebview = window.idepy
  window.dispatchEvent(new CustomEvent('pywebviewready'));
}
