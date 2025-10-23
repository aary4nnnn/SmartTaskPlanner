const goalForm = document.getElementById('goal-form');
        const goalInput = document.getElementById('goal-input');
        const submitButton = document.getElementById('submit-button');
        const loader = document.getElementById('loader');
        const errorMessage = document.getElementById('error-message');
        const errorText = document.getElementById('error-text');
        const resultsContainer = document.getElementById('results');
        const taskList = document.getElementById('task-list');
        const savedPlansList = document.getElementById('saved-plans-list');
        const noSavedPlansMsg = document.getElementById('no-saved-plans');
        const clearPlansButton = document.getElementById('clear-plans-button');

        const API_URL = 'http://127.0.0.1:5001/plan';
        const STORAGE_KEY = 'smartTaskPlanner_plans';

       // using local storge for storing saved task
        function getPlansFromStorage() {
            const plansJSON = localStorage.getItem(STORAGE_KEY);
            return plansJSON ? JSON.parse(plansJSON) : [];
        }

        function savePlansToStorage(plans) {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(plans));
        }

        //Display UI code
        function displayAllSavedPlans() {
            const plans = getPlansFromStorage();
            savedPlansList.innerHTML = ''; 

            if (plans.length > 0) {
                noSavedPlansMsg.classList.add('hidden');
                clearPlansButton.disabled = false;
                plans.forEach(plan => {
                    const planElement = createPlanElement(plan.goal, plan.tasks);
                    savedPlansList.appendChild(planElement);
                });
            } else {
                savedPlansList.appendChild(noSavedPlansMsg);
                noSavedPlansMsg.classList.remove('hidden');
                clearPlansButton.disabled = true;
            }
        }

        function createPlanElement(goal, tasks, isOpen = false) {
            const container = document.createElement('details');
            container.className = 'bg-white/60 rounded-xl shadow-sm border border-gray-200 overflow-hidden transition-all duration-300';
            container.open = isOpen;

            const tasksHtml = tasks.map((task, index) => {
                const colorClasses = ['bg-blue-100 text-blue-800', 'bg-green-100 text-green-800', 'bg-purple-100 text-purple-800', 'bg-orange-100 text-orange-800', 'bg-pink-100 text-pink-800'];
                const badgeColor = colorClasses[index % colorClasses.length];
                const dependenciesHtml = task.dependencies?.length
                    ? `<details class="mt-3 bg-gray-50/80 rounded-lg p-3">
                         <summary class="cursor-pointer text-sm font-semibold text-gray-700 hover:text-blue-600">
                           Show Prerequisites (${task.dependencies.length})
                         </summary>
                         <ul class="list-disc list-inside text-sm text-gray-600 mt-2 space-y-1">
                           ${task.dependencies.map(dep => `<li>${dep}</li>`).join('')}
                         </ul>
                       </details>`
                    : `<p class="mt-3 text-sm italic text-gray-500">No Prerequisites</p>`;
                return `
                <div class="task-card relative p-6 bg-white/80 border border-gray-200 rounded-2xl shadow-md">
                    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
                        <div class="flex items-center gap-3">
                            <div class="flex items-center justify-center w-10 h-10 bg-blue-600 text-white font-bold rounded-full shadow-md">${index + 1}</div>
                            <h3 class="text-lg sm:text-xl font-semibold text-gray-900">${task.task}</h3>
                        </div>
                        <span class="flex-shrink-0 ${badgeColor} text-xs font-medium px-3 py-1.5 rounded-full mt-2 sm:mt-0">${task.timeline}</span>
                    </div>
                    ${dependenciesHtml}
                </div>`;
            }).join('');

            container.innerHTML = `
                <summary class="flex justify-between items-center p-4 cursor-pointer hover:bg-gray-100/50">
                    <h3 class="text-xl font-bold text-gray-900">${goal}</h3>
                    <svg class="w-6 h-6 transform transition-transform duration-300 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
                </summary>
                <div class="p-4 border-t border-gray-200">
                    <div class="space-y-5">${tasksHtml}</div>
                </div>
            `;
            return container;
        }

        function displayNewPlan(tasks) {
            resultsContainer.classList.remove('hidden');
            taskList.innerHTML = ''; // Clear previous results
            const planElement = createPlanElement("Your New Action Plan", tasks, true); // Create it as open
            taskList.appendChild(planElement);
             
            const summary = document.createElement('div');
            summary.className = 'mt-8 text-center text-gray-700 italic';
            summary.innerHTML = `<p>✅ ${tasks.length} tasks generated and saved! See it in 'Your Saved Plans' above.</p>`;
            taskList.appendChild(summary);
        }
        
        function showError(message) {
            errorText.textContent = message;
            errorMessage.classList.remove('hidden');
        }

        //listeners made for events (Event Listeners)
        document.addEventListener('DOMContentLoaded', displayAllSavedPlans);

        clearPlansButton.addEventListener('click', () => {
            if (confirm('Are you sure you want to delete all saved plans? This cannot be undone.')) {
                localStorage.removeItem(STORAGE_KEY);
                displayAllSavedPlans();
            }
        });

        goalForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const goal = goalInput.value.trim();
            if (!goal) {
                showError("Please enter a goal before generating a plan.");
                return;
            }
            submitButton.disabled = true;
            submitButton.textContent = 'Generating...';
            resultsContainer.classList.add('hidden');
            errorMessage.classList.add('hidden');
            taskList.innerHTML = '';
            loader.classList.remove('hidden');

            try {
                const response = await fetch(API_URL, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ goal: goal }),
                });
                if (!response.ok) {
                    const errData = await response.json();
                    throw new Error(errData.error || `HTTP error! Status: ${response.status}`);
                }
                const data = await response.json();
                const planText = data.candidates?.[0]?.content?.parts?.[0]?.text;
                if (!planText) throw new Error("Could not find a valid plan in the AI response.");
                
                const plan = JSON.parse(planText);
                if (plan.tasks && plan.tasks.length > 0) {
                    const newPlan = { goal: goal, tasks: plan.tasks };
                    const allPlans = getPlansFromStorage();
                    allPlans.unshift(newPlan);
                    savePlansToStorage(allPlans);

                    displayNewPlan(plan.tasks);
                    displayAllSavedPlans();
                    goalInput.value = '';
                } else {
                    showError("The AI couldn't generate a plan for this goal. Try rephrasing it.");
                }
            } catch (error) {
                console.error('Error fetching plan:', error);
                showError(error.message || "An unknown error occurred. Make sure your backend is running.");
            } finally {
                loader.classList.add('hidden');
                submitButton.disabled = false;
                submitButton.textContent = 'Create my plan';
            }
        });
    
