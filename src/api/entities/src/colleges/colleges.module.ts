import { Module } from '@nestjs/common';
import { CollegesController } from "./colleges.controller";
import { CollegesService } from "./colleges.service";

@Module({
  providers: [CollegesService],
  controllers: [CollegesController]
})
export class CollegesModule {}
