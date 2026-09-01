<template>
    <onyks-container type="group" :class="$style.container" gap="m" align="center" justify="center">
        <img src="../assets/logo.png">
        <img src="../../node_modules/onyks-web-ui-system/dist/logo.png">
    </onyks-container>
</template>

<style module>
    .container
    {
        height: 90px;
        width: fit-content;
    }

    .container *
    {
        height: 100%;
    }
</style>