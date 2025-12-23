<script setup lang="ts">

const linksList = [
  {
    title: 'Филиалы',
    link: '/'
  },
  {
    title: 'Интеграции',
    link: '/'
  },
  {
    title: 'Статистика',
    link: '/'
  },
  {
    title: 'Прошивка',
    link: '/'
  }
];
</script>

<template>
  <q-layout view="lHh Lpr lFf">
    <q-header>
      <q-toolbar>
        <q-toolbar-title>
          App
        </q-toolbar-title>

        <q-tabs
          class="custom-tabs"
          active-class="custom-active-tab"
          indicator-class="custom-indicator"
        >
          <q-route-tab 
            flat
            v-for="link in linksList"
            :key="link.title"
            v-bind="link"
            :label="link.title"
            :to="link.link"
          />
        </q-tabs>

        <q-btn/>
        <q-btn/>

      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<style lang="scss">
  .q-toolbar {
    display: grid;
    grid-template-columns: 2fr 6fr 1fr 1fr;
    justify-content: space-between;
    align-items: center;
    background: #F5F2F2;
    color: black;
  }
</style>