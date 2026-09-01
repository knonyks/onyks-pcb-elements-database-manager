<script setup>
    import Logos from '@/components/Logos.vue';
</script>

<template>
    <onyks-container align="center" justify="center" class="container" padding="m">
        <onyks-container class="form" gap="l" padding="l">
            <Logos class="logos"></Logos>
            <onyks-text>Login</onyks-text>
            <onyks-textfield type="text"></onyks-textfield>
            <onyks-text>Password</onyks-text>
            <onyks-textfield type="password"></onyks-textfield>
            <onyks-container class="rememberMe" align="center" type="group" gap="s">
                <onyks-checkbox></onyks-checkbox>
                <onyks-text>Remember me</onyks-text>
            </onyks-container>
            
            <router-link to="/manager/dashboard" class="loginBtn"><onyks-button>Login!</onyks-button></router-link>
            
        </onyks-container>
    </onyks-container>
</template>

<style lang="css" scoped>
    .container
    {
        width: 100%;
        height: 100%;
        box-sizing: border-box;
    }

    .logos
    {
        width: 100%;
    }

    .form
    {
        max-width: 400px;
        width: 100%;
        background-color: var(--onyks-surface-1);
        border-radius: var(--onyks-radius-lg);
        border: 1px solid var(--onyks-surface-1-border);
        box-sizing: border-box;
    }

    .form > *
    {
        width: 100%;
    }

    .rememberMe
    {
        width: 100%;
    }

    .rememberMe > *
    {
        width: fit-content;
    }

    .loginBtn, .loginBtn *
    {
        width: 100%;
    }
</style>