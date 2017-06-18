import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpModule } from '@angular/http';
import { FormsModule }   from '@angular/forms';
import { RestangularModule, Restangular } from 'ngx-restangular';
import { RouterModule, Routes } from '@angular/router';
import { ModalModule } from 'ngx-bootstrap/modal';



import { AppComponent } from './app.component';
import { BucketlistComponent } from './bucketlist/bucketlist.component';
import { UsersComponent } from './users/users.component';
import { ItemsComponent } from './items/items.component';

export function RestangularConfigFactory (RestangularProvider) {
    RestangularProvider.setBaseUrl('http://127.0.0.1:5000/');
    RestangularProvider.setDefaultHeaders({'Authorization': localStorage.getItem('auth_token')});
    RestangularProvider.setRequestSuffix("/")
}
const appRoutes: Routes = [
  { path: '', component: AppComponent },
  { path: 'auth/register',component: UsersComponent },
  { path: 'auth/login',component: UsersComponent },
  { path: 'bucketlists',component: BucketlistComponent },
  ]

@NgModule({
    declarations: [
        AppComponent,
        BucketlistComponent,
        UsersComponent,
        ItemsComponent,
    ],
    imports: [
        BrowserModule,
        HttpModule,
        RestangularModule.forRoot(RestangularConfigFactory),
        FormsModule,
        RouterModule.forRoot(appRoutes),
        ModalModule.forRoot()

    ],
    providers: [],
    bootstrap: [AppComponent]
})
export class AppModule { }
