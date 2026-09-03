<script setup>
    import { ref, watch } from 'vue';
    import { onMounted, onUnmounted } from 'vue';

    const props = defineProps(
    {
        isLoading: Boolean,
        error: String,
        state: {
            type: Number,
        },
    })

    const isFinishing = ref(false)
    const color = ref('red')
    let finishTimer = null

    const randomColor = () =>
    {
        let colors = ['red', 'blue', 'green', 'yellow', 'gray']
        return colors[Math.floor(Math.random() * colors.length)]
    }

    color.value = randomColor()

    watch(() => props.isLoading, (isLoading) => 
    {
        if (finishTimer) 
        {
            clearTimeout(finishTimer)
        }

        if (isLoading) 
        {
            isFinishing.value = false
            return
        }

        isFinishing.value = true

        finishTimer = setTimeout(() => 
        {
            finishTimer = setTimeout(() => 
            {
                isFinishing.value = false
            }, 350)
        }, 250)
    }, { immediate: true })
</script>

<template>
    <transition name="fade" mode="out-in">

        <onyks-container v-if="isLoading || isFinishing" align="center" justify="center" class="loadingBar" padding="l">
            <onyks-loading-bar max="100" :current-state="props.state" :color="color" size="xl" striped animated></onyks-loading-bar>
        </onyks-container>

        <onyks-container v-else-if="error" align="center" justify="center" padding="l" class="error">
            <onyks-alert  type="error">{{ error }}</onyks-alert>
        </onyks-container>
        
        <onyks-container v-else padding="m" gap="l">
            <slot></slot>
        </onyks-container>

    </transition>
</template>

<style scoped>
    .loadingBar
    {
        width: 100%;
        height: 20%;
        box-sizing: border-box;
        z-index: 100;
        position: static;
    }

    onyks-loading-bar
    {
        max-width: 500px;
    }

    .error
    {
        width: 100%;
        height: fit-content;
        box-sizing: border-box;
        z-index: 100;
        position: static;
    }

    .error > onyks-alert
    {
        width: 100%;
    }

    .fade-enter-active, .fade-leave-active 
    {
        transition: opacity 0.3s ease;
    }

    .fade-enter-from, .fade-leave-to 
    {
        opacity: 0;
    }
</style>