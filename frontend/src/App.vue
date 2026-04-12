<script setup>
</script>

<template>
    <onyks-nav size="m">
        <onyks-logo></onyks-logo>
        <onyks-nav-content maxviewitems="5">
            <!-- <router-link to="/dashboard"><onyks-nav-option :selected="$route.path === '/dashboard'">Dashboard</onyks-nav-option></router-link> -->
            <!-- <router-link to="/management"><onyks-nav-option :selected="$route.path === '/management'">Management</onyks-nav-option></router-link> -->
            <router-link to="/repository"><onyks-nav-option :selected="$route.path === '/repository'">Repository</onyks-nav-option></router-link>
            <!-- <router-link to="/settings"><onyks-nav-option :selected="$route.path === '/settings'">Settings</onyks-nav-option></router-link> -->
            <!-- <router-link to="/admin"><onyks-nav-option :selected="$route.path === '/admin'">Admin</onyks-nav-option></router-link> -->
        </onyks-nav-content>
    </onyks-nav>

    <main>
        <router-view v-slot="{ Component, route }">
            <transition name="fade" mode="out-in">
                <div :key="route.path">
                    <component :is="Component" />
                </div>
            </transition>
        </router-view>
    </main>
</template>

<style scoped>
onyks-nav
  {
    position: sticky;
    top: 0;
    margin: 0;
    width: auto;
    z-index: 100000;
  }

  onyks-nav > onyks-logo
  {
    position: absolute;
    left: 0;
    height: 100%;
    box-sizing: border-box;
    padding: var(--spacing-md);
    top: 0;
    width: fit-content;
  }

  main
  {
    max-width: 1024px;
    margin-left: auto;
    margin-right: auto;
    min-height: 90vh;
    box-sizing: border-box;
    padding: var(--spacing-lg);
  }

  a
  {
    text-decoration: none;
    color: inherit;
  }

    .fade-enter-active, .fade-leave-active 
    {
        transition: opacity 0.2s ease;
    }

    .fade-enter-from, .fade-leave-to 
    {
        opacity: 0;
    }
</style>