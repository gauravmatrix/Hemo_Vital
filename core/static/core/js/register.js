// /* ===================================================================
//    HemoVital - Final Registration Wizard JavaScript
//    Handles multi-step navigation, role switching, and frontend validation.
//    =================================================================== */

// (function () {
//     'use strict';

//     document.addEventListener('DOMContentLoaded', function () {

//         // ==========================================
//         //  STATE & DOM ELEMENTS
//         // ==========================================
//         const state = {
//             currentStep: 1,
//             totalSteps: 3,
//             currentRole: 'user', // 'user' or 'hospital'
//         };

//         const dom = {
//             roleSelector: document.getElementById('masterRoleSelector'),
//             userForm: document.getElementById('user-form'),
//             hospitalForm: document.getElementById('hospital-form'),
//             prevBtn: document.getElementById('prevStepBtn'),
//             nextBtn: document.getElementById('nextStepBtn'),
//             progressSteps: document.querySelectorAll('.progress-step'),
//             stepTitleDisplay: document.getElementById('step-title-display'),
//             currentStepDisplay: document.getElementById('current-step-display'),
//         };

//         // ==========================================
//         //  CORE FUNCTIONS
//         // ==========================================

//         /**
//          * Updates the entire UI based on the current state.
//          * This includes progress bar, buttons, and visible step.
//          */
//         function updateUI() {
//             const activeForm = state.currentRole === 'user' ? dom.userForm : dom.hospitalForm;
            
//             // 1. Update Progress Bar
//             dom.progressSteps.forEach((stepEl, index) => {
//                 const stepNum = index + 1;
//                 stepEl.classList.remove('active', 'completed');
//                 if (stepNum < state.currentStep) {
//                     stepEl.classList.add('completed');
//                 } else if (stepNum === state.currentStep) {
//                     stepEl.classList.add('active');
//                 }
//             });

//             // 2. Show the correct step (fieldset) within the active form
//             const steps = activeForm.querySelectorAll('.wizard-step');
//             steps.forEach(stepEl => {
//                 stepEl.style.display = 'none';
//                 stepEl.classList.remove('active');
//             });
//             const currentStepEl = activeForm.querySelector(`.wizard-step[data-step="${state.currentStep}"]`);
//             if (currentStepEl) {
//                 currentStepEl.style.display = 'block';
//                 currentStepEl.classList.add('active');
//                 // Update the step title
//                 const title = currentStepEl.querySelector('.step-title').textContent;
//                 if(dom.stepTitleDisplay) dom.stepTitleDisplay.textContent = title;
//                 if(dom.currentStepDisplay) dom.currentStepDisplay.textContent = state.currentStep;
//             }

//             // 3. Update Navigation Buttons
//             dom.prevBtn.style.display = state.currentStep > 1 ? 'flex' : 'none';
//             if (state.currentStep === state.totalSteps) {
//                 dom.nextBtn.innerHTML = 'Create Account <i class="fas fa-check"></i>';
//                 // Important: Change button type to 'submit' on the last step
//                 dom.nextBtn.setAttribute('type', 'submit'); 
//             } else {
//                 dom.nextBtn.innerHTML = 'Next Step <i class="fas fa-arrow-right"></i>';
//                  // Important: Keep button type as 'button' to prevent form submission
//                 dom.nextBtn.setAttribute('type', 'button');
//             }
//         }

//         /**
//          * Switches the active form between 'user' and 'hospital'.
//          * @param {string} role - The role to switch to ('user' or 'hospital').
//          */
//         function handleRoleChange(role) {
//             state.currentRole = role;
//             state.currentStep = 1;

//             if (role === 'user') {
//                 dom.userForm.style.display = 'block';
//                 dom.hospitalForm.style.display = 'none';
//             } else {
//                 dom.userForm.style.display = 'none';
//                 dom.hospitalForm.style.display = 'block';
//             }
//             updateUI();
//         }

//         /**
//          * Validates only the required inputs within the current active step.
//          * @returns {boolean} - True if the step is valid, otherwise false.
//          */
//         function validateCurrentStep() {
//             let isValid = true;
//             const activeForm = state.currentRole === 'user' ? dom.userForm : dom.hospitalForm;
//             const currentStepEl = activeForm.querySelector('.wizard-step.active');
            
//             const inputs = currentStepEl.querySelectorAll('input[required], select[required], textarea[required]');

//             inputs.forEach(input => {
//                 const parentGroup = input.closest('.form-group');
//                 const errorMsgEl = parentGroup.querySelector('.input-error-message');
                
//                 if (!input.value || (input.type === 'checkbox' && !input.checked)) {
//                     isValid = false;
//                     parentGroup.classList.add('has-error');
//                     if(errorMsgEl) errorMsgEl.textContent = 'This field is required.';
//                 } else {
//                      parentGroup.classList.remove('has-error');
//                      if(errorMsgEl) errorMsgEl.textContent = '';
//                 }
//             });
//             return isValid;
//         }


//         // ==========================================
//         //  EVENT HANDLERS
//         // ==========================================

//         function handleNext() {
//             if (state.currentStep < state.totalSteps) {
//                 if (validateCurrentStep()) {
//                     state.currentStep++;
//                     updateUI();
//                 }
//             }
//             // If it's the last step, the button type is 'submit',
//             // so the form will submit naturally if validation passes.
//         }

//         function handlePrev() {
//             if (state.currentStep > 1) {
//                 state.currentStep--;
//                 updateUI();
//             }
//         }
        
//         /**
//          * On the final step, this function ensures the correct form is submitted.
//          */
//         function handleSubmit(event) {
//             // This function is triggered when the nextBtn (as a submit button) is clicked
//             if (!validateCurrentStep()) {
//                 event.preventDefault(); // Stop form submission if validation fails
//                 console.error("Validation failed on the last step.");
//             } else {
//                  const activeForm = state.currentRole === 'user' ? dom.userForm : dom.hospitalForm;
//                  activeForm.submit();
//             }
//         }


//         // ==========================================
//         //  INITIALIZATION
//         // ==========================================
//         function init() {
//             // Role switcher
//             dom.roleSelector.addEventListener('change', (e) => {
//                 if(e.target.name === 'registration_role') {
//                     handleRoleChange(e.target.value);
//                 }
//             });

//             // Navigation buttons
//             dom.nextBtn.addEventListener('click', (e) => {
//                 if(e.target.type === 'submit') {
//                     handleSubmit(e);
//                 } else {
//                     handleNext();
//                 }
//             });
//             dom.prevBtn.addEventListener('click', handlePrev);
            
//             // Initial UI setup
//             handleRoleChange(state.currentRole);
//         }

//         init();
//     });
// })();

