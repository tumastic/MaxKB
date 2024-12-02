import Layout from '@/layout/layout-template/DetailLayout.vue'
const functionLibRouter = {
  path: '/function-lib',
  name: 'function-lib',
  meta: { title: '函数库', permission: 'APPLICATION:READ' },
  redirect: '/function-lib1',
  component: () => import('@/layout/layout-template/AppLayout.vue'),
  children: [
    {
      path: '/function-lib1',
      name: 'function-lib1',
      component: () => import('@/views/function-lib/index.vue')
    }
  ]
}

export default functionLibRouter
