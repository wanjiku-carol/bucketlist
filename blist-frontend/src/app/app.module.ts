import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpModule } from '@angular/http';
import { FormsModule }   from '@angular/forms';
import { RestangularModule, Restangular } from 'ngx-restangular';
import { RouterModule, Routes } from '@angular/router';
import { MomentModule } from 'angular2-moment';
import {Ng2PaginationModule} from 'ng2-pagination';


import { AppComponent } from './app.component';
import { BucketlistsComponent } from './bucketlists/bucketlists.component';
import { ItemsComponent } from './items/items.component';

export function RestangularConfigFactory (RestangularProvider) {
    RestangularProvider.setBaseUrl('http://127.0.0.1:5000/');
    RestangularProvider.setDefaultHeaders({'Authorization': localStorage.getItem('auth_token')});
    RestangularProvider.setRequestSuffix("/")
}
const appRoutes: Routes = [
  { path: '', component: AppComponent },
  { path: 'bucketlists/:id', component: ItemsComponent },
  { path: 'bucketlists', component: BucketlistsComponent },
  ]


@NgModule({
  declarations: [
    AppComponent,
    BucketlistsComponent,
    ItemsComponent,
  ],
  imports: [
    BrowserModule,
    BrowserModule,
    HttpModule,
    RestangularModule.forRoot(RestangularConfigFactory),
    FormsModule,
    RouterModule.forRoot(appRoutes),
    MomentModule,
    Ng2PaginationModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
