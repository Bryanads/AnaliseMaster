(function () {
  "use strict";

  var tablist = document.querySelector('[role="tablist"]');
  if (!tablist) return;

  var tabs = Array.prototype.slice.call(tablist.querySelectorAll('[role="tab"]'));
  var panels = tabs.map(function (tab) {
    return document.getElementById(tab.getAttribute("aria-controls"));
  });

  function activate(index) {
    tabs.forEach(function (tab, i) {
      var selected = i === index;
      tab.setAttribute("aria-selected", selected ? "true" : "false");
      tab.tabIndex = selected ? 0 : -1;
    });
    panels.forEach(function (panel, i) {
      if (!panel) return;
      panel.hidden = i !== index;
    });
  }

  function focusTab(index) {
    var next = (index + tabs.length) % tabs.length;
    tabs[next].focus();
    activate(next);
  }

  tablist.addEventListener("click", function (e) {
    var t = e.target.closest('[role="tab"]');
    if (!t || !tablist.contains(t)) return;
    var idx = tabs.indexOf(t);
    if (idx >= 0) activate(idx);
  });

  tablist.addEventListener("keydown", function (e) {
    var current = tabs.indexOf(document.activeElement);
    if (current < 0) return;
    if (e.key === "ArrowRight" || e.key === "ArrowDown") {
      e.preventDefault();
      focusTab(current + 1);
    } else if (e.key === "ArrowLeft" || e.key === "ArrowUp") {
      e.preventDefault();
      focusTab(current - 1);
    } else if (e.key === "Home") {
      e.preventDefault();
      tabs[0].focus();
      activate(0);
    } else if (e.key === "End") {
      e.preventDefault();
      tabs[tabs.length - 1].focus();
      activate(tabs.length - 1);
    }
  });

  var initial = tabs.findIndex(function (tab) {
    return tab.getAttribute("aria-selected") === "true";
  });
  if (initial < 0) initial = 0;
  activate(initial);
})();
