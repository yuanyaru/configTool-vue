<template>
  <el-container>
    <el-aside :width="isCollapse?'45px':'220px'">
      <el-menu :default-openeds="[]" :collapse="isCollapse">
        <el-submenu index="1">
          <template slot="title"><i class="el-icon-message"></i>导航一</template>
          <el-menu-item-group>
            <template slot="title">分组一</template>
            <el-menu-item index="1-1">选项1</el-menu-item>
            <el-menu-item index="1-2">选项2</el-menu-item>
          </el-menu-item-group>
          <el-menu-item-group title="分组2">
            <el-menu-item index="1-3">选项3</el-menu-item>
          </el-menu-item-group>
          <el-submenu index="1-4">
            <template slot="title">选项4</template>
            <el-menu-item index="1-4-1">选项4-1</el-menu-item>
          </el-submenu>
        </el-submenu>
        <el-submenu index="2">
          <template slot="title"><i class="el-icon-menu"></i>导航二</template>
          <el-menu-item-group>
            <template slot="title">分组一</template>
            <el-menu-item index="2-1">选项1</el-menu-item>
            <el-menu-item index="2-2">选项2</el-menu-item>
          </el-menu-item-group>
          <el-menu-item-group title="分组2">
            <el-menu-item index="2-3">选项3</el-menu-item>
          </el-menu-item-group>
          <el-submenu index="2-4">
            <template slot="title">选项4</template>
            <el-menu-item index="2-4-1">选项4-1</el-menu-item>
          </el-submenu>
        </el-submenu>
        <el-submenu index="3">
          <template slot="title"><i class="el-icon-setting"></i>导航三</template>
          <el-menu-item-group>
            <template slot="title">分组一</template>
            <el-menu-item index="3-1">选项1</el-menu-item>
            <el-menu-item index="3-2">选项2</el-menu-item>
          </el-menu-item-group>
          <el-menu-item-group title="分组2">
            <el-menu-item index="3-3">选项3</el-menu-item>
          </el-menu-item-group>
          <el-submenu index="3-4">
            <template slot="title">选项4</template>
            <el-menu-item index="3-4-1">选项4-1</el-menu-item>
          </el-submenu>
        </el-submenu>
      </el-menu>
    </el-aside>
    
    <el-container>
      <el-header style="text-align: right; font-size: 12px">
        <div class="header-fold">
          <i v-if="!isCollapse" class="el-icon-s-fold" @click="isCollapse=!isCollapse"></i>
          <i v-if="isCollapse" class="el-icon-s-unfold" @click="isCollapse=!isCollapse"></i>
          <span>****</span>
        </div> 
        <div class="screenfull" @click="screenfullclick">
          <i class="el-icon-full-screen"></i>
          <span>{{ isscreenfull ? '退出全屏' : '全屏' }}</span>
        </div>
        <div class="refresh" @click="refresh">
          <i class="el-icon-refresh"></i>
          <span @click="refresh">刷新</span>
        </div>
      </el-header>
      
      <el-main>
        <vxe-grid
          border
          resizable
          keep-source
          ref="xGrid"
          id="toolbar_demo_1"
          height="500"
          :print-config="{}"
          :import-config="{}"
          :export-config="{}"
          :columns="tableColumn"
          :toolbar-config="tableToolbar"
          :data="tableData"
          :custom-config="{storage: true}"
          :edit-config="{trigger: 'click', mode: 'row', showStatus: true}"
          @toolbar-button-click="toolbarButtonClickEvent"
          @toolbar-tool-click="toolbarToolClickEvent">
        </vxe-grid>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import screenfull from "screenfull"
import "./css/style.css";

export default {
  data() {
    return {
      isCollapse: false,
      isscreenfull: false,
      tableData: [],
      tableToolbar: {
        refresh: true,
        import: true,
        export: true,
        print: true,
        zoom: true,
        custom: true
      },
      tableColumn: []
    }
  },
  watch: {
  },
  mounted () {
  },
  created () {
  },
  methods: {
    toolbarToolClickEvent ({ code }) {
      const $grid = this.$refs.xGrid
      switch (code) {
        case 'myPrint':
          $grid.print()
          break
      }
    },

    screenfullclick() {
      // 判断是否支持
      if (!screenfull.enabled) {
        console.dir('不支持全屏')
      }
      this.isscreenfull = !this.isscreenfull
      screenfull.toggle();
    },

    refresh() {
      location.reload();
    },
  },
}
</script>