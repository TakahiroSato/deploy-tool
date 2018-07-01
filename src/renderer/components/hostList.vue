<template>
  <div id="left-pane">
    <ul>
        <li class="left-pane" v-for="host in hosts" v-bind:key="host" @click="selectHost(host)">{{ host }}</li>
    </ul>
  </div>
</template>

<script>
  export default {
    name: 'host-list',
    props: ['hosts'],
    methods: {
      selectHost: function (host) {
        this.$emit('selectHost', host)
      }
    }
  }
</script>

<style>
  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  body { font-family: 'Source Sans Pro', sans-serif; }

  #left-pane {
    width: 150px;
    height: inherit;
    display: inline-block;
    float:left;
    text-align: center;
    border-style: solid;
    border-color: gray;
    border-width: 0 1px 0 0;
  }

  li.left-pane{
    width:100%;
    padding-top:5px;
    padding-bottom:5px;
    border-bottom: 1px solid #999999;
    color:red;
  }

  ul{
    text-align: center;
  }
</style>
