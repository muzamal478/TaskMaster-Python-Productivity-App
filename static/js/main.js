// main.js - UI helpers for TaskMaster dark theme
(function(){
  // Theme toggle (persists in localStorage)
  const themeToggle = document.getElementById('themeToggle');
  const themeIcon = document.getElementById('themeIcon');

  function setTheme(mode){
    if(mode === 'light'){
      document.documentElement.setAttribute('data-bs-theme','light');
      document.body.classList.remove('bg-dark'); document.body.classList.add('bg-light');
      themeIcon.className = 'fa fa-moon';
      localStorage.setItem('tm_theme','light');
    } else {
      document.documentElement.setAttribute('data-bs-theme','dark');
      document.body.classList.remove('bg-light'); document.body.classList.add('bg-dark');
      themeIcon.className = 'fa fa-sun';
      localStorage.setItem('tm_theme','dark');
    }
  }

  // init theme
  const saved = localStorage.getItem('tm_theme') || 'dark';
  setTheme(saved);

  if(themeToggle){
    themeToggle.addEventListener('click', (e) => {
      const curr = localStorage.getItem('tm_theme') || 'dark';
      setTheme(curr === 'dark' ? 'light' : 'dark');
    });
  }

  // Reminders: improved throttle + readable notification
  async function checkReminders(){
    try {
      const res = await fetch('/api/tasks');
      if(!res.ok) return;
      const tasks = await res.json();
      const now = new Date();
      const notifyList = tasks.filter(t => t.reminder && !t.completed && t.due_date).filter(t => {
        const d = new Date(t.due_date);
        // notify if within next 15 minutes or overdue by up to 1 hour
        return (d - now) <= (15*60*1000) && (d - now) >= -60*60*1000;
      });
      if(notifyList.length === 0) return;
      if(Notification.permission === 'default') await Notification.requestPermission();
      if(Notification.permission === 'granted'){
        notifyList.forEach(t => {
          const body = `${t.title} — due ${new Date(t.due_date).toLocaleString()}`;
          new Notification('TaskMaster Reminder', { body });
        });
      }
    } catch (err) {
      // silent fail
      console.debug('Reminder check failed', err);
    }
  }

  // run on load + every 5 minutes
  checkReminders();
  setInterval(checkReminders, 5 * 60 * 1000);

})();
