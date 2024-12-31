document.addEventListener("DOMContentLoaded", () => {
    const userNameField = document.getElementById("user_name");
    const userIdField = document.getElementById("user_id");
    const wakeTimeField = document.getElementById("wake_time");
    const bedtimeField = document.getElementById("bedtime");
    const sleepDurationField = document.getElementById("sleep_duration");
    const errorContainer = document.getElementById("error-message");
    const form = document.getElementById("schedule-form");

    function showError(message) {
        errorContainer.innerHTML = message;
        errorContainer.classList.remove("d-none");
    }

    function hideError() {
        errorContainer.innerHTML = "";
        errorContainer.classList.add("d-none");
    }

    function validateUserName() {
        const userName = userNameField.value.trim();
        if (!userName) {
            showError("Name is required.");
            return false;
        }
        hideError();
        return true;
    }

    function validateUserId() {
        const userId = userIdField.value.trim();
        if (!userId) {
            showError("User ID is required.");
            return false;
        }
        hideError();
        return true;
    }

    function validateTimes() {
        const wakeTime = wakeTimeField.value;
        const bedtime = bedtimeField.value;

        if (!wakeTime || !bedtime) {
            showError("Both wake time and bedtime are required.");
            return false;
        }

        const wakeTimeObj = new Date(`1970-01-01T${wakeTime}:00`);
        let bedtimeObj = new Date(`1970-01-01T${bedtime}:00`);

        if (bedtimeObj <= wakeTimeObj) {
            bedtimeObj.setDate(bedtimeObj.getDate() + 1);
        }

        if (bedtimeObj <= wakeTimeObj) {
            showError("Bedtime must be after wake time.");
            return false;
        }

        hideError();
        return true;
    }

    function validateSleepDuration() {
        const sleepDuration = parseInt(sleepDurationField.value, 10);
        if (!sleepDuration || sleepDuration < 4 || sleepDuration > 10) {
            showError("Sleep duration must be between 4 and 10 hours.");
            return false;
        }
        hideError();
        return true;
    }

    form.addEventListener("submit", (event) => {
        const isValidName = validateUserName();
        const isValidId = validateUserId();
        const isValidTimes = validateTimes();
        const isValidSleepDuration = validateSleepDuration();

        if (!isValidName || !isValidId || !isValidTimes || !isValidSleepDuration) {
            event.preventDefault();
        }
    });
});
