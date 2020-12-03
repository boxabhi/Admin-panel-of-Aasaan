<template>
    <div>


        <input type="checkbox" id="sidebar-toggle">
        <div class="sidebar">
            <v-navigation-drawer class="deep-purple accent-4" dark permanent style="background : #027581 !important">
                <h3 class="brand mt-5 pt-5 text-center">
                    <span class="ti-bolt"></span>
                    <span>Aasaan</span>
                </h3>
                <v-list>
                    <v-list-item v-for="item in items" :key="item.title" link>

                       <v-list-item-icon>
                            <v-icon>{{ item.icon }}</v-icon>
                        </v-list-item-icon>
                        <router-link :to="`/${item.link}`">
                           <a href="">
                                
                            <v-list-item-content>
                                <v-list-item-title class="text-white" style="color:#fff !important">{{ item.title }}
                                </v-list-item-title>
                            </v-list-item-content>
                           </a>
                        </router-link>
                    </v-list-item>
                </v-list>

    <div class="container ml-5">
        <router-link to="/">
        <a href="">
        <v-btn color="green" class="ml-5"  @click="signout">Logout</v-btn>
        </a>
        </router-link>
    </div>
            </v-navigation-drawer>
        
        </div>


        <div class="main-content">

            <header>
                <div class="search-wrapper">
                    <span class="ti-search"></span>
                    <input type="search" placeholder="Search">
                </div>

                <div class="social-icons">
                    <span @click="signout" class="ti-power-off"></span>
                    <div></div>
                </div>
            </header>

            <main>
                <slot name="main-content"></slot>
            </main>

        </div>
    </div>
</template>

<script>
    export default {
        name: 'DashboardLayout',
        data() {
            return {
                items: [
                    {
                        title: 'Dashboard',
                        icon: 'mdi-view-dashboard',
                        link: 'dashboard'
                    },
                    {
                        title: 'Super',
                        icon: 'mdi-flower',
                        link: 'super'
                    },

                     {
                        title: 'Question',
                        icon: 'mdi-comment-question-outline',
                        link: 'question'
                    },
                    {
                        title: 'Category',
                        icon: ' mdi-clipboard-outline',
                        link: 'category'
                    },
                      {
                        title: 'Notifications',
                        icon: 'mdi-bell',
                        link: 'notifications'
                    },
                    {
                        title: 'Admins',
                        icon: 'mdi-account-settings',
                        link: 'admin/create'
                    },
                    {
                        title: 'Users',
                        icon: 'mdi-account',
                        link: 'users'
                    },
                      {
                        title: 'Password',
                        icon: 'mdi-key',
                        link: 'password'
                    },
                    {
                        title: 'Image Gallery',
                        icon: 'mdi-key',
                        link: 'upload-image'
                    },
                    {
                        title: 'Requests',
                        icon: 'mdi-chili-mild',
                        link: 'requests'
                    }
                   
                   
                    
                   

                ],
            }
        },
        methods: {
            signout() {
                localStorage.removeItem('admin')
              
                this.$router.push('/');
            }
        }
    }
</script>