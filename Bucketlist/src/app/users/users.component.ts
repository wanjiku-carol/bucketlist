import { Component, OnInit } from '@angular/core';
// import { UsersService } from './users.service';
import { RestangularModule, Restangular } from 'ngx-restangular';

@Component({
  selector: 'app-users',
  templateUrl: './users.component.html',
  styleUrls: ['./users.component.css'],
  // providers: [UsersService]
})
export class UsersComponent {
    allAccounts;
    accounts;
    account;


  constructor(private restangular: Restangular) { }

  ngOnInit() {
      let baseUrl = this.restangular.all('auth/register');

      let addAccount = baseUrl.post({'username':'potatoes','email':'potatoes@email.com','password':'potatoes_123'});
  }

}
