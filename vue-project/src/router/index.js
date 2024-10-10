import ClientsView from '@/views/ClientsView.vue'
import OrdersView from '@/views/OrdersView.vue'
import ShoppingcartView from '@/views/ShoppingcartView.vue'
import ProductsView from '@/views/ProductsView.vue'
import ReviewView from '@/views/ReviewView.vue'
import { createRouter, createWebHistory } from 'vue-router'
import CategoryView from '@/views/CategoryView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "OrdersView",
      component: OrdersView,
    },
    {
      path: "/clients",
      name: "ClientsView",
      component: ClientsView,
    }
    ,
    {
      path: "/shoppingcarts",
      name: "ShoppingcartView",
      component: ShoppingcartView,
    },
    {
      path: "/products",
      name: "ProductsView",
      component: ProductsView,
    },
    {
      path: "/reviews",
      name: "ReviewView",
      component: ReviewView,
    },
    {
      path: "/categories",
      name: "CategoryView",
      component: CategoryView,
    }
  ]
})

export default router
