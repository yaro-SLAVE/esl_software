<script setup lang="ts">

const linksList = [
  {
    title: 'Филиалы',
    link: '/filials'
  },
  {
    title: 'Интеграция',
    link: '/integration'
  },
  {
    title: 'Статистика',
    link: '/statistics'
  },
  {
    title: 'Прошивка',
    link: '/firmware'
  }
];
</script>

<template>
  <q-layout view="lHh Lpr lFf">
    <q-header>
      <q-toolbar>
        <q-toolbar-title>
          Quasar App
        </q-toolbar-title>

        <div class="row">
          <q-btn 
            flat
            v-for="link in linksList"
            :key="link.title"
            v-bind="link"
            :label="link.title"
            :to="link.link"
          />
        </div>

        <q-btn/>
        <q-btn/>

      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<style lang="css">
  .q-toolbar {
    display: grid;
    grid-template-columns: 2fr 6fr 1fr 1fr;
    justify-content: space-between;
    align-items: center;
    background: #F5F2F2;
    color: black;
  }
</style>