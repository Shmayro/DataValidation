import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UnitverifComponent } from './unitverif.component';

describe('UnitverifComponent', () => {
  let component: UnitverifComponent;
  let fixture: ComponentFixture<UnitverifComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ UnitverifComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(UnitverifComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
