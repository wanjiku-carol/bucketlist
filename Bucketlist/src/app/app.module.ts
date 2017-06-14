import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpModule } from '@angular/http';
import { RestangularModule, Restangular } from 'ngx-restangular';


import { AppComponent } from './app.component';
import { BucketlistComponent } from './bucketlist/bucketlist.component';
import { UsersComponent } from './users/users.component';

export function RestangularConfigFactory (RestangularProvider) {
  RestangularProvider.setBaseUrl('http://127.0.0.1:5000/');
  RestangularProvider.setDefaultHeaders({'Authorization': localStorage.getItem('auth_token')});
  RestangularProvider.setRequestSuffix("/")
}

@NgModule({
  declarations: [
    AppComponent,
    BucketlistComponent,
    UsersComponent
  ],
  imports: [
    BrowserModule, HttpModule, RestangularModule.forRoot(RestangularConfigFactory)
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
