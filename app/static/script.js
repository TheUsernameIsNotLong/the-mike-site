// shamefully, this code was ai generated - i have no true intention of learning javascript lol

document.addEventListener("DOMContentLoaded", () => {
  const tabs = document.querySelectorAll('[role="tab"]');
  const tabPanels = document.querySelectorAll('[role="tabpanel"]');

  tabs.forEach(tab => {
      tab.addEventListener("click", () => {
          // Deactivate all tabs
          tabs.forEach(t => {
              t.setAttribute("aria-selected", "false");
          });

          // Hide all panels
          tabPanels.forEach(panel => {
              panel.hidden = true;
          });

          // Activate clicked tab
          tab.setAttribute("aria-selected", "true");
          const tabPanel = document.getElementById(tab.getAttribute("aria-controls"));
          tabPanel.hidden = false;
      });
  });
});