import { BlistFrontendPage } from './app.po';

describe('blist-frontend App', () => {
  let page: BlistFrontendPage;

  beforeEach(() => {
    page = new BlistFrontendPage();
  });

  it('should display welcome message', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('Welcome to app!!');
  });
});
