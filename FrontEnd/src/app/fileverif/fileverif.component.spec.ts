import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FileverifComponent } from './fileverif.component';

describe('FileverifComponent', () => {
  let component: FileverifComponent;
  let fixture: ComponentFixture<FileverifComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ FileverifComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(FileverifComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
