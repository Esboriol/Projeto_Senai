// Toggle do menu do usuário (autoclose ao clicar fora)
    (function(){
      const btn = document.getElementById('userBtn');
      const menu = document.getElementById('userMenu');
      if (!btn || !menu) return;

      btn.addEventListener('click', function(e){
        e.stopPropagation();
        const shown = menu.classList.toggle('show');
        btn.setAttribute('aria-expanded', shown ? 'true' : 'false');
        menu.setAttribute('aria-hidden', shown ? 'false' : 'true');
      });

      document.addEventListener('click', function(){
        if (menu.classList.contains('show')){
          menu.classList.remove('show');
          btn.setAttribute('aria-expanded', 'false');
          menu.setAttribute('aria-hidden', 'true');
        }
      });

      // Fecha com ESC
      document.addEventListener('keydown', function(e){
        if (e.key === 'Escape' && menu.classList.contains('show')){
          menu.classList.remove('show');
          btn.setAttribute('aria-expanded', 'false');
          menu.setAttribute('aria-hidden', 'true');
        }
      });
    })();