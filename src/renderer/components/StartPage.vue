<template>
  <div id="wrapper">
    <ul class="tab-selector">
      <li class="tab-selector" v-for="(tab, index) in tabNav" @click="changeTab(index)" v-bind:class="{ active: index === contents }">{{ tab }}</li>
    </ul>
    <div v-bind:style="{ clear:'both', height: height-30 + 'px' }">
      <div v-if="contents == 0" class="tab-content">
        <ConnectionSettingPage />
      </div>
      <div v-if="contents == 1" class="tab-content">
        <DeployPage />
      </div>
    </div>
  </div>
</template>

<script>
  import ConnectionSettingPage from './TabPage/ConnectionSettingPage'
  import DeployPage from './TabPage/DeployPage'

  export default {
    name: 'start-page',
    components: {
      ConnectionSettingPage,
      DeployPage
    },
    data: function () {
      return {
        tabNav: [
          '接続先設定',
          'デプロイ'
        ],
        contents: 0,
        height: 574
      }
    },
    methods: {
      changeTab: function (index) {
        this.contents = index
      },
      handleResize: function () {
        this.height = window.innerHeight - 24
      }
    },
    mounted: function () {
      this.height = window.innerHeight - 24
      window.addEventListener('resize', this.handleResize)
    },
    beforeDestroy: function () {
      window.removeEventListener('resize', this.handleResize)
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

  #wrapper{
    width: 100vw;
    height: 100vh;
  }

  li{
    display:block;
    float:left;
    width: 100px;
    text-align: center;
  }

  li.active{
    background: #aaaaaa;
  }

  ul.tab-selector{
    display:inline-block;
    margin-bottom: 5px;
  }

  li.tab-selector{
    border:2px solid #999999;
    margin-right: 5px;
    background:#dddddd;
  }

  .tab-content{
    height: inherit;
  }
</style>
