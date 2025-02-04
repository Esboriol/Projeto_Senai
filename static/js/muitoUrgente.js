document.addEventListener('DOMContentLoaded', () => {
    // Nome da conta logada
    const nomeConta = "Dev"; // Substitua pelo nome real da conta logada

    // Atualiza o texto do campo com o ID "nome"
    const nomeElement = document.getElementById('nome');
    if (nomeElement) {
        nomeElement.textContent = nomeConta;
    }

   const cardData = [
//       { title: "Problema 1", content: "Equipamento de climatização quebrado. Necessário verificar o sistema de resfriamento e aquecimento.", status: "finished" },
//       { title: "Problema 2", content: "Fiação elétrica exposta no corredor principal. Precisa de inspeção imediata para evitar riscos de choque.", status: "most-urgent" },
//       { title: "Problema 3", content: "Vazamento na tubulação do banheiro. Verificar e reparar a tubulação para evitar danos maiores.", status: "urgent" },
//       { title: "Problema 4", content: "Janela do escritório com problemas de fechamento. Substituir ou ajustar o mecanismo de fechamento.", status: "common" },
//       { title: "Problema 5", content: "Interruptor de luz não funcionando na sala de reunião. Substituir o interruptor.", status: "no-status" },
//       { title: "Problema 6", content: "Sistema de alarme de incêndio desativado. Verificar e garantir que o sistema esteja operacional.", status: "finished" },
//       { title: "Problema 7", content: "Porta de entrada com fechadura defeituosa. Precisa de reparo ou substituição da fechadura.", status: "most-urgent" },
//       { title: "Problema 8", content: "Sistema de irrigação do jardim não está funcionando. Verificar bombas e tubulações.", status: "urgent" },
//       { title: "Problema 9", content: "Luminárias do corredor precisam de substituição. Substituir lâmpadas queimadas e verificar circuitos.", status: "common" },
//       { title: "Problema 10", content: "Computador do servidor com falha de hardware. Realizar diagnóstico e substituição de peças defeituosas.", status: "no-status" },
//       { title: "Problema 11", content: "Ar condicionado do escritório central está inoperante. Agendar manutenção ou reparo urgente.", status: "finished" },
//       { title: "Problema 12", content: "Fugas de gás detectadas na cozinha. Contatar serviços de emergência e reparar vazamento.", status: "most-urgent" },
//       { title: "Problema 13", content: "Piso da área de armazenamento está danificado. Reparo necessário para evitar acidentes.", status: "urgent" },
//       { title: "Problema 14", content: "Equipamentos de TI na sala de servidores estão superaquecendo. Verificar sistemas de ventilação.", status: "common" },
//       { title: "Problema 15", content: "Porta de saída de emergência com mecanismo de travamento defeituoso. Verificar e reparar.", status: "no-status" }
//
   ];

   const container = document.getElementById('card-container');
   const containerHU = document.getElementById('card-container-HU');
   const highUrgencyCards = cardData.filter(card => card.status === 'most-urgent');
  
   // Define a ordem dos status
   const statusPriority = {
       'most-urgent': 1,
       'urgent': 2,
       'common': 3,
       'finished': 4,
       'no-status': 5
   };

   // Define a cor de fundo para cada status
   const statusColors = {
       'finished': '#28a745',
       'most-urgent': '#dc3545',
       'urgent': '#ffc107',
       'common': '#007bff',
       'no-status': '#6c757d'
   };
 /*   highUrgencyCards.forEach(cardInfo => {
       const card = document.createElement('div');
       card.className = 'card';

       const cardTitle = document.createElement('h2');
       cardTitle.textContent = cardInfo.title;

       const cardContent = document.createElement('p');
       cardContent.textContent = cardInfo.content;

       const cardStatus = document.createElement('div');
       cardStatus.className = `status ${cardInfo.status}`;
       cardStatus.textContent = cardInfo.status.replace(/-/g, ' ').toUpperCase(); // Exibe o status com palavras em maiúsculas e substitui hífens por espaços

       card.appendChild(cardTitle);
       card.appendChild(cardContent);
       card.appendChild(cardStatus);

       containerHU.appendChild(card);
   }); */

   
   // Ordena os dados dos cards com base na prioridade do status
   highUrgencyCards.sort((a, b) => statusPriority[a.status] - statusPriority[b.status]);

   // Adiciona todos os cards ao contêiner
   highUrgencyCards.forEach(cardInfo => {
//       const card = document.createElement('div');
//       card.className = 'card';
//
//       const cardTitle = document.createElement('h2');
//       cardTitle.textContent = cardInfo.title;
//
//       const cardContent = document.createElement('p');
//       cardContent.textContent = cardInfo.content;
//
//       const cardStatus = document.createElement('div');
//       cardStatus.className = `status ${cardInfo.status}`;
//       cardStatus.textContent = cardInfo.status.replace(/-/g, ' ').toUpperCase(); // Exibe o status com palavras em maiúsculas e substitui hífens por espaços
//
//       const statusSelect = document.createElement('div');
//       statusSelect.className = 'status-select';
//
//       const select = document.createElement('select');
//       const statuses = [
//           { value: 'finished', label: 'Finalizado' },
//           { value: 'most-urgent', label: 'Muito Urgente' },
//           { value: 'urgent', label: 'Urgente' },
//           { value: 'common', label: 'Comum' },
//           { value: 'no-status', label: 'Sem Status' }
//       ];
//
//       statuses.forEach(status => {
//           const option = document.createElement('option');
//           option.value = status.value;
//           option.textContent = status.label;
//           select.appendChild(option);
//       });

       select.value = cardInfo.status;
       select.style.backgroundColor = statusColors[cardInfo.status]; // Define a cor de fundo com base no status atual

       select.addEventListener('change', (event) => {
           const newStatus = event.target.value;
           cardStatus.className = `status ${newStatus}`;
           cardStatus.textContent = newStatus.replace(/-/g, ' ').toUpperCase(); // Atualiza o texto do status

           // Atualiza a cor de fundo do seletor
           select.style.backgroundColor = statusColors[newStatus];

           // Atualiza o status no cardData
           cardInfo.status = newStatus;

           // Reordena os cards após a atualização
           const cards = Array.from(container.children);
           cards.sort((a, b) => statusPriority[a.querySelector('.status').className.split(' ')[1]] - statusPriority[b.querySelector('.status').className.split(' ')[1]]);
           cards.forEach(card => container.appendChild(card)); // Reanexa os cards ordenados
       });

       statusSelect.appendChild(select);
       
       card.appendChild(cardTitle);
       card.appendChild(cardContent);
       card.appendChild(cardStatus);
       card.appendChild(statusSelect);

       containerHU.appendChild(card);
   });
});
