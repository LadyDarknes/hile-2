let stockfish;
const globalVariable = { currentTabId: null }; // biraz kötü ama idare eder :DDD

let currentRound = 0;

var attachedTabs = {};
var version = '1.3';
var letsdo = null;
var debugIdGlobal;

let debuggerEnabled = false;

var xC, yC;

const sendMessageToContentJs = (tabId, message) => {
  chrome.tabs.sendMessage(tabId, message);
};

Stockfish().then((sf) => {
  stockfish = sf;
  sf.addMessageListener((message) => {
    sendMessageToContentJs(globalVariable.currentTabId, {
      type: 'stockfish',
      message: message,
      round: currentRound,
    });
  });
});

chrome.runtime.onMessage.addListener((message, senderInfo, reply) => {
  globalVariable.currentTabId = senderInfo.tab.id;
  if (message.type === 'stockfish') {
    if (message.position) {
      stockfish.postMessage(message.position);
    }
    if (message.message.includes('go depth')) {
      stockfish.postMessage('ucinewgame');
    }
    stockfish.postMessage(message.message);
  }
  if (message.eventPlease === 'trusted') {
    if (debuggerEnabled) {
      reply({ yourEvent: 'Görev etkinleştiriliyor, biraz bekleyin' });

      xC = message.x;
      yC = message.y;
      if (message.mouse == 'D') {
        chrome.debugger.sendCommand(
          { tabId: senderInfo.tab.id },
          'Input.dispatchMouseEvent',
          { type: 'mousePressed', x: xC, y: yC, button: 'left', clickCount: 1 },
          function (e) {}
        );
      } else if (message.mouse == 'U') {
        chrome.debugger.sendCommand(
          { tabId: senderInfo.tab.id },
          'Input.dispatchMouseEvent',
          {
            type: 'mouseReleased',
            x: xC,
            y: yC,
            button: 'left',
            clickCount: 1,
          },
          function (e) {}
        );
      }
    } else {
      reply({
        yourEvent: 'Lütfen otomatik hareketi etkinleştirin',
      });
    }
  } else if (message.type === 'start') {
    var tabId = senderInfo.tab.id;
    var debuggeeId = { tabId: tabId };
    debugIdGlobal = debuggeeId;

    if (!attachedTabs[tabId]) {
      chrome.debugger.attach(
        debuggeeId,
        version,
        onAttach.bind(null, debuggeeId)
      );
    }
  } else if (message.type === 'pause') {
    var tabId = senderInfo.tab.id;
    var debuggeeId = { tabId: tabId };
    debugIdGlobal = debuggeeId;

    if (attachedTabs[tabId]) {
      chrome.debugger.detach(debuggeeId, onDetach.bind(null, debuggeeId));
    }
  }
});

chrome.debugger.onEvent.addListener(onEvent);
chrome.debugger.onDetach.addListener(onDetach);

function onAttach(debuggeeId) {
  if (chrome.runtime.lastError) {
    alert(chrome.runtime.lastError.message);
    return;
  }

  tabId = debuggeeId.tabId;
  attachedTabs[tabId] = 'working';
  chrome.debugger.sendCommand(
    debuggeeId,
    'Debugger.enable',
    {},
    onDebuggerEnabled.bind(null, debuggeeId)
  );
}

function onDebuggerEnabled(debuggeeId) {
  debuggerEnabled = true;
}

function onDebuggerDisabled(debuggeeId) {
  debuggerEnabled = false;
}

function onEvent(debuggeeId, method, frameId, resourceType) {
  tabId = debuggeeId.tabId;
  if (method == 'Debugger.paused') {
    attachedTabs[tabId] = 'paused';
  }
}

function onDetach(debuggeeId) {
  var tabId = debuggeeId.tabId;
  chrome.debugger.sendCommand(
    debuggeeId,
    'Debugger.disable',
    {},
    onDebuggerDisabled.bind(null, debuggeeId)
  );
  delete attachedTabs[tabId];
  debuggerEnabled = false;
  chrome.storage.local.set({ automove: false });
}
