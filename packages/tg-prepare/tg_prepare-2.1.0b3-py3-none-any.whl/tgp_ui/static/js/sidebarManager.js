define([], function () {
    const SidebarManager = {
        sidebar: document.querySelector("#sidebar"),

        toggleSidebar: function () {
            this.sidebar.classList.toggle("expand");
        },

        checkSidebarVisibility: function () {
            const isCurrentlyVisible = window.innerWidth >= 1080;
            this.sidebar.classList.toggle("expand", isCurrentlyVisible);
        },

        init: function () {
            // Toggle Sidebar on Button Click
            document.querySelector(".toggle-btn").addEventListener("click", () => {
                this.toggleSidebar();
            });

            // Check Sidebar Visibility on Resize
            window.addEventListener("resize", () => {
                this.checkSidebarVisibility();
            });

            // Initial Sidebar Visibility Check
            this.checkSidebarVisibility();

        }
    };

    return SidebarManager;
});