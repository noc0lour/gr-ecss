/* -*- c++ -*- */
/*
 * Copyright 2018 Antonio Miraglia - ISISpace.
 *
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifndef INCLUDED_ECSS_NRZL_ENCODER_IMPL_H
#define INCLUDED_ECSS_NRZL_ENCODER_IMPL_H

#include <ecss/nrzl_encoder.h>

namespace gr {
  namespace ecss {

    class nrzl_encoder_impl : public nrzl_encoder
    {
     private:
      float *positive;
      float *negative;
      int d_interpolation;

     public:
      nrzl_encoder_impl(float bit_rate, float samp_rate);
      ~nrzl_encoder_impl();

      // Where all the action really happens
      int work(int noutput_items,
         gr_vector_const_void_star &input_items,
         gr_vector_void_star &output_items);
    };

  } // namespace ecss
} // namespace gr

#endif /* INCLUDED_ECSS_NRZL_ENCODER_IMPL_H */

